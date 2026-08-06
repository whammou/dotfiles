# tabfreeze.py - freeze hidden tabs via QWebEnginePage lifecycle states.
# qutebrowser 3.7.0 has no built-in tab freezing; this emulates the Chromium
# "page lifecycle" behavior by setting the QtWebEngine page state directly.
import os
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt.core import QEvent, QMetaObject, QObject, QTimer, Qt, pyqtSlot
from qutebrowser.qt.gui import QPixmap, QWindow
from qutebrowser.qt.webenginecore import QWebEnginePage
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
# "L" while a hidden tab is still loading (freeze deferred until done).
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


def _apply_state() -> None:
    try:
        _apply_window_states()
    except Exception:
        log.misc.exception("tabfreeze: state pass failed")


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
                    page.setVisible(True)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                    log.misc.debug("tabfreeze: %s -> Active (exempt)", host or url)
                parts.append(f"{window.win_id}.{i}:- {host or url}")
                continue
            win_handle = window.windowHandle()
            if config.val.tabs.tabs_are_windows:
                # Every tab is its own OS window. qtile-wayland hides one by
                # disabling its scene node (qw/xdg-view.c: qw_xdg_view_hide);
                # the surface survives, so Qt keeps the handle and reports
                # the loss of exposure instead. A missing handle means Qt
                # never showed the window at all. Either way, not exposed
                # means it is not on screen.
                visible = win_handle is not None and win_handle.isExposed()
            else:
                # Only the current tab of a tab bar is rendered.
                visible = i == widget.currentIndex()
            state = (
                QWebEnginePage.LifecycleState.Active
                if visible
                else QWebEnginePage.LifecycleState.Frozen
            )
            page = tab._widget.page()
            live = page.lifecycleState()
            if id(tab) not in _load_hooked:
                signal = getattr(tab, "load_status_changed", None)
                if signal is not None:
                    signal.connect(_apply_state)
                    _load_hooked.add(id(tab))
            # Freezing a page mid-navigation stalls the load and the engine
            # rejects the state change, so defer until the load is done. A
            # fresh tab reports load_status "success" from its initial blank
            # page before the real navigation starts, so an empty URL means
            # it has not loaded anything yet either.
            loading = (
                state == QWebEnginePage.LifecycleState.Frozen
                and (
                    url.isEmpty()
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
                # the first attempt after a hide can fail silently; every
                # later pass (expose, focus change, tab switch) retries it
                # instead of waiting out a rate limit.
                widget = tab._widget
                if state == QWebEnginePage.LifecycleState.Frozen:
                    _drop_overlay(widget)
                else:
                    _show_overlay(widget, _previews.pop(id(widget), None))
                    QTimer.singleShot(600, lambda: _capture_preview(id(widget), widget))
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
                # finish, the load_status_changed hook re-freezes it after.
                page.setVisible(True)
                page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                log.misc.debug("tabfreeze: %s -> Active (load pending)", host or url)
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
    if label is not None:
        label.deleteLater()


def _show_overlay(widget: Any, preview: QPixmap | None) -> None:
    if preview is None or preview.isNull():
        return
    label = QLabel(widget)
    label.setPixmap(preview)
    label.setGeometry(widget.rect())
    label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    label.show()
    label.raise_()
    _overlays[id(widget)] = label
    QTimer.singleShot(500, lambda: _expire_overlay(id(widget), label))


def _expire_overlay(widget_id: int, label: QLabel) -> None:
    if _overlays.get(widget_id) is label:
        _overlays.pop(widget_id, None)
        label.deleteLater()


def _capture_preview(widget_id: int, widget: Any) -> None:
    # QtWebEngine renders via a QQuickWidget, whose textures live in the
    # window's QRhi; grabbing during the compositor hide/teardown races
    # the QRhi swap ("texture belongs to QRhi X, used with QRhi Y"), so
    # the frame for the next freeze is captured here, on the visible side.
    try:
        if _previews.get(widget_id) is not None:
            return
        handle = widget.windowHandle()
        if handle is not None and handle.isExposed():
            _previews[widget_id] = widget.grab()
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
