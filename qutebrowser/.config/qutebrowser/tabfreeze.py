# tabfreeze.py - freeze unfocused tabs via QWebEnginePage lifecycle states.
# The last rendered frame is pinned over a frozen tab, so a window that is
# visible but unfocused keeps showing its last viewport instead of going
# blank. State follows focus only: revealing a window never unfreezes it.
# qutebrowser 3.7.0 has no built-in tab freezing; this emulates the Chromium
# "page lifecycle" behavior by setting the QtWebEngine page state directly.
import os
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt import sip
from qutebrowser.qt.core import QEvent, QMetaObject, QObject, QTimer, Qt, pyqtSlot
from qutebrowser.qt.gui import QPixmap, QWindow
from qutebrowser.qt.webenginecore import QWebEngineLoadingInfo, QWebEnginePage
from qutebrowser.qt.widgets import QLabel
from qutebrowser.utils import log, objreg
from qutebrowser.utils.usertypes import LoadStatus

# Pages whose renderer must never be frozen (devtools and internal pages).
_SKIP_SCHEMES = {"qute", "chrome", "devtools", "view-source"}

# Domains that must never be frozen; a subdomain of an exempt domain is
# exempt too ("example.com" also exempts "www.example.com"). sites.py can
# add its own via the FREEZE_EXEMPT_DOMAINS environment variable.
_EXEMPT_DOMAINS = set()


def _exempt_domains() -> set[str]:
    # qutebrowser purges sys.modules entries added while sourcing a config
    # file (configfiles.saved_sys_properties), so sites.py passes its list
    # through the process environment instead, which survives.
    domains = set(_EXEMPT_DOMAINS)
    raw = os.environ.get("FREEZE_EXEMPT_DOMAINS", "")
    domains.update(d for d in raw.split(",") if d)
    return domains


def _is_exempt(host: str, exempt: set[str]) -> bool:
    return host in exempt or host.endswith(tuple("." + d for d in exempt))

# Letters for the per-pass summary log: actual page lifecycle state, or
# "L" while an unfocused tab is still loading (freeze deferred until done).
_LIVE_LETTERS = {
    QWebEnginePage.LifecycleState.Active: "A",
    QWebEnginePage.LifecycleState.Frozen: "F",
    QWebEnginePage.LifecycleState.Discarded: "D",
}

_hooked: set[int] = set()
_load_hooked: set[int] = set()
_frozen_seen: set[int] = set()
_previews: dict[int, QPixmap] = {}
_overlays: dict[int, QLabel] = {}
# Monotonic time (widget id) when the engine first reported Active after
# an unfreeze; the pin stays up for a settle window so the first fresh
# frame is presented underneath it, not a stale one.
_active_since: dict[int, float] = {}
# The engine flips its lifecycle state to Active before it presents the
# first fresh frame (state reacts to activation, painting comes later),
# so the pin must outlive the state change by this margin.
_SETTLE_SECONDS = 0.3
# Pages the engine reports as currently loading (engine-truth, because
# qutebrowser's load_status lags urlChanged and can stay "success" from
# a tab's initial blank page while a real navigation is in flight).
_loading_pages: set[int] = set()


def _apply_state() -> None:
    try:
        _apply_window_states()
    except Exception:
        log.misc.exception("tabfreeze: state pass failed")


def _on_loading_changed(page, info: QWebEngineLoadingInfo) -> None:
    if info.status() == QWebEngineLoadingInfo.LoadStatus.LoadStartedStatus:
        _loading_pages.add(id(page))
    else:
        _loading_pages.discard(id(page))
    _apply_state()


def _apply_window_states() -> None:
    parts: list[str] = []
    exempt = _exempt_domains()
    for window in objreg.window_registry.values():
        widget = window.tabbed_browser.widget
        for i in range(widget.count()):
            tab = widget.widget(i)
            if tab is None or tab.data.pinned or tab.url().scheme() in _SKIP_SCHEMES:
                continue
            url = tab.url()
            host = url.host()
            if _is_exempt(host, exempt):
                page = tab._widget.page()
                if page.lifecycleState() != QWebEnginePage.LifecycleState.Active:
                    _drop_overlay(tab._widget)
                    page.setVisible(True)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                    log.misc.debug("tabfreeze: %s -> Active (exempt)", host or url)
                parts.append(f"{window.win_id}.{i}:- {host or url}")
                continue
            win_handle = window.windowHandle()
            if config.val.tabs.tabs_are_windows:
                # Every tab is its own window; the one receiving key events
                # is active. When the whole app loses focus none is active,
                # so every tab freezes.
                focused = win_handle is not None and win_handle.isActive()
            else:
                # Only the current tab of a focused window is active.
                focused = (
                    win_handle is not None
                    and win_handle.isActive()
                    and i == widget.currentIndex()
                )
            state = (
                QWebEnginePage.LifecycleState.Active
                if focused
                else QWebEnginePage.LifecycleState.Frozen
            )
            page = tab._widget.page()
            live = page.lifecycleState()
            widget = tab._widget
            if id(tab) not in _load_hooked:
                signal = getattr(tab, "load_status_changed", None)
                if signal is not None:
                    signal.connect(_apply_state)
                page.loadingChanged.connect(
                    lambda info, page=page: _on_loading_changed(page, info)
                )
                page.destroyed.connect(
                    lambda _obj=None, page=page: _loading_pages.discard(id(page))
                )
                _load_hooked.add(id(tab))
            # Freezing a page mid-navigation stalls the load and the engine
            # rejects the state change, so defer until the load is done. A
            # fresh tab reports load_status "success" from its initial blank
            # page before the real navigation starts, so an empty URL means
            # it has not loaded anything yet either; the engine's own
            # loadingChanged signal is the authoritative in-flight check.
            loading = (
                state == QWebEnginePage.LifecycleState.Frozen
                and (
                    url.isEmpty()
                    or id(page) in _loading_pages
                    or tab.load_status in (LoadStatus.none, LoadStatus.loading)
                )
            )
            parts.append(
                f"{window.win_id}.{i}:"
                f"{'L' if loading and live != QWebEnginePage.LifecycleState.Frozen else _LIVE_LETTERS.get(live, '?')} "
                f"{host or url}"
            )
            if live != state and not loading:
                # Retry on every pass: QtWebEngine ignores lifecycle
                # changes until its visibility update has propagated, so
                # the first attempt after an unfocus can fail silently;
                # every later pass retries it instead of waiting out a
                # rate limit.
                if state == QWebEnginePage.LifecycleState.Frozen:
                    # Pin the last rendered frame before freezing: a frozen
                    # page stops painting, so without this the window would
                    # go blank while visible-but-unfocused. Grabbing is safe
                    # here because losing focus keeps the window mapped,
                    # unlike a compositor hide/teardown. The previous
                    # preview is kept until a fresh capture succeeds, so a
                    # window hidden on another qtile group (which cannot be
                    # grabbed, see _capture_preview) still has a frame to
                    # pin instead of flashing blank on reveal.
                    _drop_overlay(widget)
                    _capture_preview(id(widget), widget)
                    preview = _previews.get(id(widget))
                    if preview is not None and not preview.isNull():
                        _show_overlay(widget, preview)
                    elif win_handle is not None and win_handle.isExposed():
                        # Visible but no frame to pin: freezing would leave
                        # the window blank, so stay Active and retry.
                        state = QWebEnginePage.LifecycleState.Active
                    # A window that is not exposed cannot be seen, so it
                    # freezes without a pin; the reveal branch pins it
                    # later if it becomes visible while still unfocused.
                else:
                    # Focus came back: the page renders again, so unpin the
                    # last frame shortly after.
                    _expire_overlay_soon(id(widget))
                # QtWebEngine rejects lifecycle changes while its own page
                # visibility flag says the page is visible; on qtile-wayland
                # setVisible is independent of the window's isExposed().
                page.setVisible(state == QWebEnginePage.LifecycleState.Active)
                page.setLifecycleState(state)
                log.misc.debug("tabfreeze: %s -> %s", host or url, state)
            elif (
                live == QWebEnginePage.LifecycleState.Frozen and loading
            ):
                # A navigation was already in flight when this tab froze
                # (freeze raced the first load); resume so the load can
                # finish, the loadingChanged hook re-freezes it after.
                _drop_overlay(widget)
                page.setVisible(True)
                page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                log.misc.debug("tabfreeze: %s -> Active (load pending)", host or url)
            elif loading and not page.isVisible():
                # Load in flight while unfocused: the engine activates the
                # page to load but does not restore visibility itself, so a
                # freeze from before the navigation would leave it blank.
                page.setVisible(True)
            elif (
                live == QWebEnginePage.LifecycleState.Frozen
                and win_handle is not None
                and win_handle.isExposed()
                and id(widget) not in _overlays
                and (
                    config.val.tabs.tabs_are_windows
                    or i == widget.currentIndex()
                )
            ):
                # Revealed (mapped) while unfocused: the tab froze while it
                # was hidden, so pin its frame now; only focus unfreezes.
                if id(widget) not in _previews:
                    _capture_preview(id(widget), widget)
                preview = _previews.get(id(widget))
                if preview is not None and not preview.isNull():
                    _show_overlay(widget, preview)
            if (
                live == QWebEnginePage.LifecycleState.Frozen
                and id(tab) not in _frozen_seen
            ):
                _frozen_seen.add(id(tab))
                log.misc.info("tabfreeze: frozen %s", host or url)
            elif live != QWebEnginePage.LifecycleState.Frozen:
                _frozen_seen.discard(id(tab))
    log.misc.debug("tabfreeze: %s", "  ".join(parts) or "-")


def _drop_overlay(widget: Any) -> None:
    label = _overlays.pop(id(widget), None)
    _active_since.pop(id(widget), None)
    # The tab window may have been closed since the overlay was shown,
    # destroying the C++ label; deleteLater() on it would raise.
    if label is not None and not sip.isdeleted(label):
        label.deleteLater()


def _show_overlay(widget: Any, preview: QPixmap | None) -> None:
    if preview is None or preview.isNull():
        log.misc.debug("tabfreeze: overlay skipped (no valid preview)")
        return
    label = QLabel(widget)
    label.setPixmap(preview)
    label.setGeometry(widget.rect())
    label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    label.show()
    label.raise_()
    _overlays[id(widget)] = label
    log.misc.debug(
        "tabfreeze: overlay shown %sx%s on %sx%s",
        preview.width(), preview.height(),
        widget.width(), widget.height(),
    )


def _expire_overlay_soon(widget_id: int) -> None:
    label = _overlays.get(widget_id)
    if label is not None:
        QTimer.singleShot(500, lambda: _expire_overlay(widget_id, label))


def _expire_overlay(widget_id: int, label: QLabel) -> None:
    if _overlays.get(widget_id) is not label:
        return
    if sip.isdeleted(label):
        _overlays.pop(widget_id, None)
        return
    parent = label.parent()
    page = None
    if parent is not None and not sip.isdeleted(parent):
        page = getattr(parent, "page", lambda: None)()
    if (
        page is not None
        and not sip.isdeleted(page)
        and page.lifecycleState() != QWebEnginePage.LifecycleState.Active
    ):
        # The engine is still unfreezing, so the pin must stay up: if it
        # came off now the stale frame would flash before the first new
        # paint arrives. Retry instead of deleting.
        QTimer.singleShot(150, lambda: _expire_overlay(widget_id, label))
        return
    if page is not None and not sip.isdeleted(page):
        # The engine reported Active before presenting the first fresh
        # frame (state flips on activation, painting comes later), so the
        # pin stays up for a settle window from the first Active report
        # and the stale frame is covered by the new one, not flashed.
        since = _active_since.get(widget_id)
        if since is None:
            _active_since[widget_id] = time.monotonic()
            QTimer.singleShot(150, lambda: _expire_overlay(widget_id, label))
            return
        elif time.monotonic() - since < _SETTLE_SECONDS:
            QTimer.singleShot(150, lambda: _expire_overlay(widget_id, label))
            return
    _active_since.pop(widget_id, None)
    _overlays.pop(widget_id, None)
    # The expiry timer can outlive the tab window: closing it destroys
    # the C++ label, so deleteLater() on it would raise.
    if not sip.isdeleted(label):
        label.deleteLater()


def _capture_preview(widget_id: int, widget: Any) -> None:
    # QtWebEngine renders via a QQuickWidget, whose textures live in the
    # window's QRhi; grabbing during the compositor hide/teardown races
    # the QRhi swap ("texture belongs to QRhi X, used with QRhi Y"), so
    # the frame is only captured while the window is still mapped.
    try:
        # tab._widget is a non-native child, so windowHandle() is null on
        # it; the top-level MainWindow owns the actual QWindow.
        top = widget.window()
        handle = top.windowHandle() if top is not None else None
        if handle is not None and handle.isExposed():
            _previews[widget_id] = widget.grab()
            pic = _previews[widget_id]
            log.misc.debug(
                "tabfreeze: capture win=%s exposed null=%s %sx%s",
                handle.winId(), pic.isNull(), pic.width(), pic.height(),
            )
        else:
            log.misc.debug(
                "tabfreeze: capture skipped handle=%s exposed=%s",
                handle is not None,
                handle.isExposed() if handle is not None else None,
            )
    except Exception:
        log.misc.exception("tabfreeze: preview capture failed")


class _ExposeFilter(QObject):

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if (
            a0 is not None
            and a1 is not None
            and a1.type() == QEvent.Type.Expose
            and isinstance(a0, QWindow)
        ):
            log.misc.debug("tabfreeze: expose %s", a0.winId())
            _apply_state()
        return False


_expose_filter = _ExposeFilter()


def _wire_window(window) -> None:
    try:
        widget = window.tabbed_browser.widget
        wid = id(widget)
        if wid in _hooked:
            return
        _hooked.add(wid)
        widget.currentChanged.connect(_apply_state)
        window.tabbed_browser.new_tab.connect(lambda _tab, _idx: _apply_state())
        widget.destroyed.connect(lambda: _hooked.discard(wid))
        log.misc.debug("tabfreeze: monitoring window %d", window.win_id)
        _apply_state()
    except Exception:
        log.misc.exception("tabfreeze: wiring window failed")


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            # Group switches move focus and every new window announces
            # itself, so all state changes arrive as events: no polling.
            # QtWayland reports compositor hide/reveal as QEvent.Expose on
            # the QWindow, which is a separate object from the MainWindow
            # widget, so the filter has to be global on the app.
            objects.qapp.installEventFilter(_expose_filter)
            objects.qapp.new_window.connect(_wire_window)
            objects.qapp.focusWindowChanged.connect(lambda _win: _apply_state())
            for window in objreg.window_registry.values():
                _wire_window(window)
        except Exception:
            log.misc.exception("tabfreeze: arm failed")


def _wait_for_app() -> None:
    # Daemon thread: at interpreter shutdown the objects module is torn
    # down while this thread may still be polling; any error then is
    # irrelevant (the process is exiting), just stop quietly.
    try:
        while objects.qapp is None:
            time.sleep(0.1)
        QMetaObject.invokeMethod(
            _scheduler, "arm", Qt.ConnectionType.QueuedConnection
        )
    except Exception:
        return


_scheduler = _Scheduler()
threading.Thread(target=_wait_for_app, daemon=True).start()
