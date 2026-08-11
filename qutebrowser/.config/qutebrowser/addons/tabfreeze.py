# tabfreeze.py - freeze unfocused tabs via QWebEnginePage lifecycle states.
# The last rendered frame is pinned over a frozen tab, so a window that is
# visible but unfocused keeps showing its last viewport instead of going
# blank. Focus alone does not unfreeze either: a focused window's tab
# stays pinned until its first key/mouse/wheel input. qutebrowser 3.7.0
# has no built-in tab freezing; this emulates the Chromium
# "page lifecycle" behavior by setting the QtWebEngine page state directly.
import hashlib
import os
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt import sip
from qutebrowser.qt.core import (
    QEvent, QMetaObject, QObject, QSize, QTimer, Qt, pyqtSlot,
)
from qutebrowser.qt.gui import QImage, QPixmap, QWindow
from qutebrowser.qt.webenginecore import (
    QWebEngineLoadingInfo,
    QWebEnginePage,
)
from qutebrowser.qt.widgets import QLabel, QWidget
from qutebrowser.utils import log, objreg
from qutebrowser.utils.usertypes import LoadStatus

# Pages whose renderer must never be frozen (devtools and internal pages).
_SKIP_SCHEMES = {"qute", "chrome", "devtools", "view-source"}

# Domains that must never be frozen; a subdomain of an exempt domain is
# exempt too ("example.com" also exempts "www.example.com"). sites.py can
# add its own via the FREEZE_EXEMPT_DOMAINS environment variable.
_EXEMPT_DOMAINS = set()


# qutebrowser purges sys.modules entries added while sourcing a config
# file (configfiles.saved_sys_properties), so sites.py passes its list
# through the process environment instead, which survives; that bridge
# only changes at config-source, so the parsed set is memoized on the
# raw string.
_exempt_raw: str | None = None
_exempt_cache: set[str] = set()


def _exempt_domains() -> set[str]:
    global _exempt_raw
    raw = os.environ.get("FREEZE_EXEMPT_DOMAINS", "")
    if raw != _exempt_raw:
        _exempt_cache.clear()
        _exempt_cache.update(_EXEMPT_DOMAINS)
        _exempt_cache.update(d for d in raw.split(",") if d)
        _exempt_raw = raw
    return _exempt_cache


def _is_exempt(host: str, exempt: set[str]) -> bool:
    return host in exempt or host.endswith(tuple("." + d for d in exempt))


# qutebrowser answers permission prompts via the legacy
# setFeaturePermission() API, which never writes to the engine's
# permission store (queryPermission always returns Ask), so grants are
# read from qutebrowser's own config instead. Cached per origin; the
# config-source re-exec resets the cache.
_CAPTURE_OPTIONS = (
    "content.media.audio_capture",
    "content.media.video_capture",
    "content.media.audio_video_capture",
    "content.desktop_capture",
)
_capture_ok: dict[str, bool] = {}


def _capture_granted(url: Any) -> bool:
    # A fresh tab's empty URL cannot carry a permission grant, and
    # qutebrowser's config lookup rejects invalid URLs with an
    # exception, so skip the lookup.
    if not url.isValid():
        return False
    origin = f"{url.scheme()}://{url.host()}"
    if origin in _capture_ok:
        return _capture_ok[origin]
    granted = False
    try:
        granted = any(
            config.instance.get(option, url=url) is True
            for option in _CAPTURE_OPTIONS
        )
    except Exception:
        # A bad URL must not fail the whole state pass; the origin is
        # cached below, so this can only fire once per origin.
        log.misc.exception("tabfreeze: capture config lookup failed")
    _capture_ok[origin] = granted
    return granted

# Letters for the per-pass summary log: actual page lifecycle state, or
# "L" while an unfocused tab is still loading (freeze deferred until done).
_LIVE_LETTERS = {
    QWebEnginePage.LifecycleState.Active: "A",
    QWebEnginePage.LifecycleState.Frozen: "F",
    QWebEnginePage.LifecycleState.Discarded: "D",
}

_hooked: set[int] = set()
_load_hooked: set[int] = set()
# Tab widget ids the module manages (for the resize filter): a tab that
# froze without ever being exposed has no pin, but must still be woken
# on resize so its first frame renders at the new size.
_tab_widgets: set[int] = set()
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
# How long an interacted window may keep reporting itself unfocused
# before its wake is cleared (see _unfocused_since).
_WAKE_GRACE_SECONDS = 0.3
# Frame poll cadence during the resize wake; slower polls grab the
# window less often.
_POLL_INTERVAL_MS = 200
# Pages the engine reports as currently loading (engine-truth, because
# qutebrowser's load_status lags urlChanged and can stay "success" from
# a tab's initial blank page while a real navigation is in flight).
_loading_pages: set[int] = set()
# Debounced re-pin state per frozen tab widget after a resize: the
# debounce timer (id -> QTimer) and the frame poll (id -> [cycle token,
# win id, attempt count, paint count, previous frame fingerprint,
# stable-frame count, changed-seen flag]) that wakes the page and waits
# for its frames to settle at the new size before re-pinning.
_resize_timers: dict[int, QTimer] = {}
_resize_polls: dict[int, tuple[Any, Any, int, int, str | None, int, bool]] = {}
# Last seen top-level window size per tab widget; a Resize whose window
# size is unchanged is an internal layout change (commandline, status or
# keyhint bar show-hide), not a real resize.
_win_sizes: dict[int, QSize] = {}

# Window ids that have received key/mouse/wheel input since their last
# focus; a focused window's tab stays pinned until its first input.
_input_seen: dict[int, bool] = {}

# Monotonic time a window was first reported unfocused. qtile-wayland
# reports the active window flakily (no window "active" between
# keypresses of a window the user is typing in), so a single bad focus
# read must not clear the wake; the flag is only popped once the window
# has been continuously unfocused for _WAKE_GRACE_SECONDS.
_unfocused_since: dict[int, float] = {}

# Signals connected while monitoring windows and tabs. The handover
# disconnects every registered pair: without this a previous module
# generation survives :config-source and keeps running state passes
# that fight the new generation over the same tabs.
_hook_conns: set[tuple[Any, Any]] = set()


def _connect(signal: Any, slot: Any) -> None:
    try:
        signal.connect(slot)
    except (RuntimeError, TypeError):
        # The receiver may have been destroyed while this file was
        # re-executed; the hook simply is not connected then.
        return
    _hook_conns.add((signal, slot))


def _apply_state() -> None:
    try:
        pending_grace = _apply_window_states()
    except Exception:
        log.misc.exception("tabfreeze: state pass failed")
        return
    if pending_grace and _state_timer is not None:
        _schedule_state()


# Coalesces event bursts (expose storms during resize drags and
# animations would otherwise run a full pass per event) into at most
# one pass per interval; the timer is created in arm() and stopped by
# the handover.
_state_timer: QTimer | None = None


def _schedule_state() -> None:
    if _state_timer is None:
        _apply_state()
    elif not _state_timer.isActive():
        _state_timer.start()


def _on_loading_changed(page, info: QWebEngineLoadingInfo) -> None:
    if info.status() == QWebEngineLoadingInfo.LoadStatus.LoadStartedStatus:
        _loading_pages.add(id(page))
    else:
        _loading_pages.discard(id(page))
    _schedule_state()


def _apply_window_states() -> bool:
    parts: list[str] = []
    pending_grace = False
    exempt = _exempt_domains()
    for window in objreg.window_registry.values():
        # A closing window leaves the registry asynchronously and can be
        # dead by the time the pass reaches it; any attribute access on
        # the wrapped MainWindow then raises RuntimeError.
        if sip.isdeleted(window):
            continue
        widget = window.tabbed_browser.widget
        win_handle = window.windowHandle()
        win_focused = win_handle is not None and win_handle.isActive()
        if not win_focused:
            # Focus reads are flaky on qtile-wayland (the compositor can
            # report no active window between keypresses of the window
            # being typed in), so a single such pass must not clear the
            # wake; only a sustained unfocused stretch does, keeping an
            # actively used window live while one truly left behind
            # still starts fresh on its next focus cycle.
            now = time.monotonic()
            if window.win_id not in _unfocused_since:
                _unfocused_since[window.win_id] = now
            elif now - _unfocused_since[window.win_id] >= _WAKE_GRACE_SECONDS:
                _input_seen.pop(window.win_id, None)
                _unfocused_since.pop(window.win_id, None)
        else:
            _unfocused_since.pop(window.win_id, None)
        interacted = _input_seen.get(window.win_id, False)
        if not win_focused and interacted:
            # The wake is still live but the window is unfocused. The
            # pass is event-driven (single-shot timer, restarted by
            # events only), and after focus left there are no more
            # events, so the pass must re-arm itself until the grace
            # expires and the tab re-freezes.
            pending_grace = True
        for i in range(widget.count()):
            tab = widget.widget(i)
            if tab is None or tab.url().scheme() in _SKIP_SCHEMES:
                continue
            url = tab.url()
            host = url.host()
            page = tab._widget.page()
            exempt_d = _is_exempt(host, exempt)
            capture = _capture_granted(url)
            # The engine call only matters when neither exemption
            # already decides the tab stays live.
            audible = (
                page.recentlyAudible()
                if not exempt_d and not capture
                else False
            )
            if exempt_d or audible or capture:
                if page.lifecycleState() != QWebEnginePage.LifecycleState.Active:
                    _drop_overlay(tab._widget)
                    page.setVisible(True)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                    log.misc.debug(
                        "tabfreeze: %s -> Active (%s)",
                        host or url,
                        "audio"
                        if audible
                        else "capture"
                        if capture
                        else "exempt",
                    )
                parts.append(
                    f"{window.win_id}.{i}:"
                    f"{'M' if audible else 'C' if capture else '-'} {host or url}"
                )
                continue
            # A window whose wake is still within its unfocused grace
            # counts as focused: isActive() can blink False between
            # keypresses, and the interaction itself proves the window
            # is the one being used.
            effective_focus = win_focused or interacted
            if config.val.tabs.tabs_are_windows:
                # Every tab is its own window; the one receiving key events
                # is active. When the whole app loses focus none is active,
                # so every tab freezes.
                focused = effective_focus
            else:
                # Only the current tab of a focused window is active.
                focused = effective_focus and i == widget.currentIndex()
            state = (
                QWebEnginePage.LifecycleState.Active
                if focused and interacted
                else QWebEnginePage.LifecycleState.Frozen
            )
            page = tab._widget.page()
            live = page.lifecycleState()
            widget = tab._widget
            if id(tab) not in _load_hooked:
                signal = getattr(tab, "load_status_changed", None)
                if signal is not None:
                    _connect(signal, _apply_state)
                _connect(
                    page.loadingChanged,
                    lambda info, page=page: _on_loading_changed(page, info),
                )
                _connect(
                    page.destroyed,
                    lambda _obj=None, page=page: _loading_pages.discard(id(page)),
                )
                _connect(
                    widget.destroyed,
                    lambda _obj=None, w=widget: _on_tab_widget_destroyed(w),
                )
                _connect(tab.pinned_changed, _schedule_state)
                _tab_widgets.add(id(widget))
                _load_hooked.add(id(tab))
            if tab.data.pinned:
                # Pinned tabs are always live: pinning is an explicit
                # "keep this alive" signal, so a tab pinned while frozen
                # (a non-current tab of a focused window, or before the
                # first-input wake) is unfrozen here; the pinned_changed
                # hook schedules this pass at pin time.
                if page.lifecycleState() != QWebEnginePage.LifecycleState.Active:
                    _drop_overlay(widget)
                    page.setVisible(True)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
                    log.misc.debug(
                        "tabfreeze: %s -> Active (pinned)", host or url
                    )
                parts.append(f"{window.win_id}.{i}:P {host or url}")
                continue
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
            if id(widget) in _resize_polls:
                # The resize wake owns this tab until its frames
                # settle; transition logic must not fight the poll
                # (a mid-wake re-freeze would blank the re-pin).
                continue
            if live != state and not loading:
                # Retry on every pass: QtWebEngine ignores lifecycle
                # changes until its visibility update has propagated, so
                # the first attempt after an unfocus can fail silently;
                # every later pass retries it instead of waiting out a
                # rate limit.
                if state == QWebEnginePage.LifecycleState.Frozen:
                    _drop_overlay(widget)
                    if win_handle is not None and win_handle.isExposed():
                        # Pin the last rendered frame before freezing: a
                        # frozen page stops painting, so without this the
                        # window would go blank while visible-but-
                        # unfocused. Grabbing is safe here because losing
                        # focus keeps the window mapped, unlike a
                        # compositor hide/teardown.
                        _capture_preview(id(widget), widget)
                        preview = _previews.get(id(widget))
                        if preview is not None and not preview.isNull():
                            _show_overlay(widget, preview)
                        else:
                            # Visible but no frame to pin: freezing would
                            # leave the window blank, so stay Active and
                            # retry.
                            state = QWebEnginePage.LifecycleState.Active
                    else:
                        # Hidden on another qtile group: nothing is
                        # visible, so no pin is needed, and any old frame
                        # can be stale (the page may have changed while
                        # hidden during a deferred load), so drop it; the
                        # reveal branch recaptures on the next map.
                        _previews.pop(id(widget), None)
                        log.misc.info(  # TEMP DEBUG: hidden, preview dropped
                            "tabfreeze: hidden win=%s tab=%d widget=%dx%d exposed=%s preview dropped",
                            window.win_id, i,
                            widget.width(), widget.height(),
                            win_handle.isExposed() if win_handle is not None else None,
                        )
                else:
                    # Focus came back: the page renders again, so unpin the
                    # last frame shortly after.
                    _expire_overlay_soon(id(widget))
                # QtWebEngine rejects lifecycle changes while its own page
                # visibility flag says the page is visible; on qtile-wayland
                # setVisible is independent of the window's isExposed().
                page.setVisible(state == QWebEnginePage.LifecycleState.Active)
                page.setLifecycleState(state)
                log.misc.info(  # TEMP DEBUG (was debug): state transition
                    "tabfreeze: %s -> %s", host or url, state
                )
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
                # Revealed (mapped) while unfocused: the tab froze while
                # hidden and has no pin, and a frozen page cannot
                # paint, so the window would stay blank until input.
                # Wake the page and re-pin once its frames settle
                # (same path as the resize wake): the fresh frame is
                # the true resumed state, so the pin matches and
                # there is no blank window. Only input unfreezes.
                log.misc.info(  # TEMP DEBUG: reveal branch firing
                    "tabfreeze: reveal win=%s tab=%d widget=%dx%d handle=%dx%d -> re_pin",
                    window.win_id, i,
                    widget.width(), widget.height(),
                    win_handle.size().width(), win_handle.size().height(),
                )
                _re_pin(widget, window.win_id)
            elif (
                live == QWebEnginePage.LifecycleState.Frozen
                and win_handle is not None
                and win_handle.isExposed()
                and id(widget) in _overlays
                and (
                    config.val.tabs.tabs_are_windows
                    or i == widget.currentIndex()
                )
            ):
                # Pin already up: steady state of a visible-but-unfocused
                # frozen tab. But a reveal can leave it stale: a bonsai
                # level-1 switch resizes the window via the compositor
                # scene graph while the client receives no QResizeEvent,
                # so _on_resized never re-pins and the old frame stays
                # stretched over the new geometry until first input.
                # Same-size steady state must not churn; only a size
                # mismatch re-pins.
                preview = _previews.get(id(widget))
                if preview is not None and preview.size() != widget.size():
                    log.misc.info(  # TEMP DEBUG: stale pin detected
                        "tabfreeze: stale pin win=%s tab=%d preview=%dx%d widget=%dx%d handle=%dx%d re_pin",
                        window.win_id, i,
                        preview.width(), preview.height(),
                        widget.width(), widget.height(),
                        win_handle.size().width(), win_handle.size().height(),
                    )
                    _win_sizes[id(widget)] = win_handle.size()
                    _re_pin(widget, window.win_id)
            if (
                live == QWebEnginePage.LifecycleState.Frozen
                and id(tab) not in _frozen_seen
            ):
                _frozen_seen.add(id(tab))
                log.misc.info("tabfreeze: frozen %s", host or url)
            elif live != QWebEnginePage.LifecycleState.Frozen:
                _frozen_seen.discard(id(tab))
    log.misc.debug("tabfreeze: %s", "  ".join(parts) or "-")
    return pending_grace


def _drop_overlay(widget: Any) -> None:
    label = _overlays.pop(id(widget), None)
    _active_since.pop(id(widget), None)
    # The tab window may have been closed since the overlay was shown,
    # destroying the C++ label; deleteLater() on it would raise.
    if label is not None and not sip.isdeleted(label):
        label.deleteLater()


def _show_overlay(widget: Any, preview: QPixmap | None) -> None:
    if preview is None or preview.isNull():
        log.misc.info(  # TEMP DEBUG (was debug): no valid preview
            "tabfreeze: overlay skipped (no valid preview)"
        )
        return
    label = QLabel(widget)
    label.setPixmap(preview)
    # Scaled so the pin stretches with the widget: a resize while frozen
    # otherwise leaves stale-size content that does not cover the window.
    label.setScaledContents(True)
    label.setGeometry(widget.rect())
    label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    label.show()
    label.raise_()
    _overlays[id(widget)] = label
    log.misc.info(  # TEMP DEBUG (was debug): overlay placed
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


def _img_fingerprint(img: Any) -> str | None:
    try:
        small = img.scaled(
            64, 64,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        return hashlib.md5(
            small.constBits().asstring(small.sizeInBytes())
        ).hexdigest()[:8]
    except Exception:
        return None


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
            log.misc.info(  # TEMP DEBUG (was debug): capture result
                "tabfreeze: capture win=%s exposed null=%s %sx%s",
                handle.winId(), pic.isNull(), pic.width(), pic.height(),
            )
        else:
            log.misc.info(  # TEMP DEBUG (was debug): capture skipped
                "tabfreeze: capture skipped handle=%s exposed=%s",
                handle is not None,
                handle.isExposed() if handle is not None else None,
            )
    except Exception:
        log.misc.exception("tabfreeze: preview capture failed")


def _on_tab_widget_destroyed(w: Any) -> None:
    _tab_widgets.discard(id(w))
    _resize_timers.pop(id(w), None)
    _resize_polls.pop(id(w), None)
    _active_since.pop(id(w), None)
    _win_sizes.pop(id(w), None)
    # A tab was killed: the layout reflows its siblings and the
    # compositor resizes them scene-graph-only (no QResizeEvent, no
    # Expose - same gap as a bonsai switch), so no pass would run and
    # the surviving pins stay stale until focus. The stale-pin check
    # needs a pass; the new geometry lands a moment after the destroy,
    # so schedule a few instead of one.
    log.misc.info(  # TEMP DEBUG: tab killed
        "tabfreeze: tab destroyed, scheduling reflow passes"
    )
    _schedule_state()
    QTimer.singleShot(100, _schedule_state)
    QTimer.singleShot(250, _schedule_state)
    QTimer.singleShot(500, _schedule_state)


def _on_resized(widget: Any) -> None:
    try:
        wid = id(widget)
        label = _overlays.get(wid)
        if label is not None:
            # The window was resized while the pin was up; a frozen page
            # cannot repaint, so stretch the pin to the new frame right
            # away, then wake the page to re-capture once it settles.
            label.setGeometry(widget.rect())
        top = widget.window()
        handle = top.windowHandle() if top is not None else None
        if handle is None or not handle.isExposed():
            log.misc.info(  # TEMP DEBUG: resize while hidden/not exposed
                "tabfreeze: resize win=%s SKIP not exposed", wid,
            )
            return
        win_size = handle.size()
        if _win_sizes.get(wid) == win_size:
            # Bar show-hide resized the layout, not the window: the pin
            # was stretched above, and waking the page would only churn
            # a grab/poll cycle for a frame that did not change.
            log.misc.info(  # TEMP DEBUG: resize with unchanged window size
                "tabfreeze: resize win=%s SKIP size unchanged", wid,
            )
            return
        _win_sizes[wid] = win_size
        page = getattr(widget, "page", lambda: None)()
        if (
            page is None
            or sip.isdeleted(page)
            or page.lifecycleState() != QWebEnginePage.LifecycleState.Frozen
        ):
            # Not frozen: the live page repaints on its own.
            return
        timer = _resize_timers.get(wid)
        if timer is None:
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: _re_pin(widget, _window_id_for(widget)))
            _resize_timers[wid] = timer
        timer.start(300)
    except Exception:
        log.misc.exception("tabfreeze: resize handling failed")


def _on_painted(widget: Any) -> None:
    wid = id(widget)
    state = _resize_polls.get(wid)
    if state is None:
        return
    token, win_id, attempts, paints, prev_fp, stable, changed_seen = state
    _resize_polls[wid] = (token, win_id, attempts, paints + 1, prev_fp, stable, changed_seen)


def _re_pin(widget: Any, win_id: int | None = None) -> None:
    try:
        wid = id(widget)
        _resize_timers.pop(wid, None)
        if sip.isdeleted(widget):
            return
        page = getattr(widget, "page", lambda: None)()
        if (
            page is None
            or sip.isdeleted(page)
            or page.lifecycleState() != QWebEnginePage.LifecycleState.Frozen
        ):
            # Not frozen anymore (focused in the meantime): the normal
            # passes own the transition.
            return
        top = widget.window()
        handle = top.windowHandle() if top is not None else None
        if handle is None or not handle.isExposed():
            return
        # The resize settled: drop the pin and wake the page so it
        # repaints at the new size. The pin must come off before the wake
        # (an overlay occludes the view, keeping its backing store stale),
        # then poll for the frame to settle before re-pinning.
        log.misc.info(
            "tabfreeze: waking %s to re-pin",
            widget.url().host() or widget.url(),
        )
        _drop_overlay(widget)
        page.setVisible(True)
        page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
        token = object()
        _resize_polls[wid] = (token, win_id, 0, 0, None, 0, False)
        QTimer.singleShot(_POLL_INTERVAL_MS, lambda t=token: _poll_re_pin(widget, t))
    except Exception:
        log.misc.exception("tabfreeze: re-pin failed")


def _poll_re_pin(widget: Any, token: Any) -> None:
    try:
        wid = id(widget)
        state = _resize_polls.get(wid)
        if (
            state is None
            or state[0] is not token
            or sip.isdeleted(widget)
        ):
            # Superseded by a newer poll cycle, or the tab is gone.
            return
        page = getattr(widget, "page", lambda: None)()
        if page is None or sip.isdeleted(page):
            _resize_polls.pop(wid, None)
            return
        if page.lifecycleState() == QWebEnginePage.LifecycleState.Frozen:
            # A state pass re-froze it during the wake (e.g. a focus
            # event): wake it again and keep polling.
            page.setVisible(True)
            page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
        _drop_overlay(widget)
        top = widget.window()
        handle = top.windowHandle() if top is not None else None
        _token, win_id, attempts, paints, prev_fp, stable, changed_seen = state
        if win_id is None:
            win_id = _window_id_for(widget)
        if win_id is not None and _input_seen.get(win_id, False):
            # The window is in use: input was already seen, or its wake
            # is still within the unfocused grace, so no pin is needed
            # and the normal transition logic owns the tab.
            _resize_polls.pop(wid, None)
            return
        # Not interacted (e.g. just switched back to this group): keep
        # polling and complete the re-pin, so the tab shows the fresh
        # frame, re-freezes, and waits for the first input instead of
        # staying live. Focus alone does not unfreeze (deferred wake).
        if handle is None or not handle.isExposed():
            # Hidden again: leave it Active for the normal passes.
            _resize_polls.pop(wid, None)
            return
        _capture_preview(wid, widget)
        pic = _previews.get(wid)
        img = pic.toImage() if pic is not None and not pic.isNull() else None
        fp = _img_fingerprint(img) if img is not None else None
        # The first poll only baselines the frame: the grab right after
        # the wake is the old frame stretched over the new geometry, and
        # settling on it pins a distorted cover. A fresh frame differs
        # from the baseline, and only then does stability count.
        if fp is not None and prev_fp is not None:
            if fp != prev_fp:
                changed_seen = True
                stable = 0
            else:
                stable += 1
        attempts += 1
        log.misc.info(  # TEMP DEBUG: re-pin frame poll
            "tabfreeze: poll win=%s attempts=%d paints=%d img=%s fp=%s stable=%d changed=%s",
            win_id, attempts, paints,
            f"{img.width()}x{img.height()}" if img is not None else "None",
            fp, stable, changed_seen,
        )
        _resize_polls[wid] = (token, win_id, attempts, paints, fp, stable, changed_seen)
        # The wake's damage repaints satisfy any paint count long before
        # the engine presents a frame at the new size, so settle on the
        # content instead: a change marks the first fresh frame, and two
        # identical polls after it mean the frame settled. A frame that
        # never changes cannot be told fresh from stale, so the attempt
        # cap pins whatever the engine last presented.
        settled = attempts >= 20 or (img is not None and changed_seen and stable >= 2)
        log.misc.info(  # TEMP DEBUG: settle decision
            "tabfreeze: settle win=%s attempts=%d paints=%d fp=%s stable=%d changed=%s settled=%s",
            win_id, attempts, paints, fp, stable, changed_seen, settled,
        )
        if not settled:
            QTimer.singleShot(_POLL_INTERVAL_MS, lambda t=token: _poll_re_pin(widget, t))
            return
        _resize_polls.pop(wid, None)
        if widget.url().isEmpty() or id(page) in _loading_pages:
            # Loading again: leave the freeze deferral to the passes.
            _schedule_state()
            return
        if page.recentlyAudible():
            # Audio started during the wake: leave the page live.
            return
        if img is None:
            # No valid frame to pin (the grab raced the engine's QRhi
            # swap or never produced content): freezing now would
            # leave the window blank, so leave the page live and let
            # the state pass retry the pin on its own schedule.
            _schedule_state()
            return
        _show_overlay(widget, QPixmap.fromImage(img))
        page.setVisible(False)
        page.setLifecycleState(QWebEnginePage.LifecycleState.Frozen)
        log.misc.info(  # TEMP DEBUG (was debug): re-pin completed
            "tabfreeze: re-pinned %s after resize",
            widget.url().host() or widget.url(),
        )
    except Exception:
        log.misc.exception("tabfreeze: re-pin failed")


class _ExposeFilter(QObject):

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if (
            a0 is not None
            and a1 is not None
            and a1.type() == QEvent.Type.Expose
            and isinstance(a0, QWindow)
            # The resize wake owns state until its frames settle, then
            # re-runs the pass itself.
            and not _resize_polls
        ):
            log.misc.info(  # TEMP DEBUG (was debug): expose event
                "tabfreeze: expose win=%s", a0.winId()
            )
            _schedule_state()
        return False


_expose_filter = _ExposeFilter()


class _ResizeFilter(QObject):

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 is None or a1 is None:
            return False
        if a1.type() == QEvent.Type.Resize and id(a0) in _tab_widgets:
            _on_resized(a0)
        elif a1.type() == QEvent.Type.Paint and _resize_polls:
            # QtWebEngine renders into a child of the tab widget, so
            # the Paint event lands on the render child, not the tab
            # widget itself; count it for the nearest polled ancestor.
            w = a0 if isinstance(a0, QWidget) else None
            while w is not None and id(w) not in _resize_polls:
                w = w.parentWidget()
            if w is not None:
                _on_painted(w)
        return False


_resize_filter = _ResizeFilter()


def _window_id_for(a0: QObject | None) -> int | None:
    """Map an event receiver to its qutebrowser window id.

    Input events are delivered to the focused widget, usually a child
    deep inside the tab, so the owning window is found by climbing the
    widget chain to the one that owns a QWindow and matching that
    handle against the registry.
    """
    if a0 is None:
        return None
    if isinstance(a0, QWindow):
        handle = a0
    else:
        handle = None
        w = a0 if isinstance(a0, QWidget) else None
        while w is not None:
            handle = w.windowHandle()
            if handle is not None:
                break
            w = w.parentWidget()
        if handle is None:
            return None
    for win_id, window in objreg.window_registry.items():
        if sip.isdeleted(window):
            continue
        win_handle = window.windowHandle()
        if win_handle is not None and win_handle.winId() == handle.winId():
            return win_id
    return None


def _active_window_id() -> int | None:
    # Only one window can hold keyboard focus, so the window whose
    # handle isActive() is the one receiving key events.
    for win_id, window in objreg.window_registry.items():
        if sip.isdeleted(window):
            continue
        win_handle = window.windowHandle()
        if win_handle is not None and win_handle.isActive():
            return win_id
    return None


class _InputFilter(QObject):
    """Records the first real input of each focused window.

    A window that refocuses after an idle keeps its tab pinned (focus
    alone does not unfreeze); the first key, mouse button or wheel
    event in the now-active window marks it interacted, which lets the
    state pass unfreeze the tab. Input on an unfocused window (pointer
    hovering a visible-but-inactive window) must not wake it.
    """

    _INPUT_TYPES = {
        QEvent.Type.KeyPress,
        QEvent.Type.MouseButtonPress,
        QEvent.Type.MouseButtonDblClick,
        QEvent.Type.Wheel,
    }

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 is None or a1 is None or a1.type() not in self._INPUT_TYPES:
            return False
        if a1.type() == QEvent.Type.KeyPress:
            # Key events are delivered to the focused widget, so the
            # receiver's widget chain locates the owning window; the
            # active-window state cannot be trusted here because
            # qtile-wayland can report no active window between
            # keypresses, and the wake would be dropped.
            win_id = _window_id_for(a0)
            if win_id is None:
                win_id = _active_window_id()
            if win_id is None:
                log.misc.info("tabfreeze: keypress while no window is active")
                return False
        else:
            win_id = _window_id_for(a0)
            if win_id is None:
                return False
            window = objreg.window_registry.get(win_id)
            if window is None or sip.isdeleted(window):
                return False
            win_handle = window.windowHandle()
            if win_handle is None or not win_handle.isActive():
                # Pointer input over an unfocused window (hover wheel,
                # a click that has not activated it yet) must not wake
                # the tab; the compositor activates the window before
                # delivering the press that focuses it.
                return False
        # Any input proves the window is being used: refresh the
        # unfocused grace so a flaky focus read cannot re-freeze it
        # mid-use. Always re-run the pass: a poll may have frozen the
        # tab after the first input, so a later input must wake it
        # again instead of being swallowed by the seen flag.
        _unfocused_since.pop(win_id, None)
        if not _input_seen.get(win_id):
            log.misc.info("tabfreeze: first input in window %d", win_id)
            _input_seen[win_id] = True
        _schedule_state()
        return False


_input_filter = _InputFilter()


def _wire_window(window) -> None:
    try:
        widget = window.tabbed_browser.widget
        wid = id(widget)
        if wid in _hooked:
            return
        _hooked.add(wid)
        _connect(widget.currentChanged, _schedule_state)
        _connect(window.tabbed_browser.new_tab, lambda _tab, _idx: _schedule_state())
        _connect(widget.destroyed, lambda: _hooked.discard(wid))
        log.misc.debug("tabfreeze: monitoring window %d", window.win_id)
        _schedule_state()
    except Exception:
        log.misc.exception("tabfreeze: wiring window failed")


def _on_focus_changed(_win) -> None:
    _schedule_state()


def _retire(old: dict) -> None:
    # qutebrowser's :config-source re-execs this file, spawning a new
    # module generation whose filters and state are fresh; the previous
    # generation's filters are still installed on the app, so it must
    # hand over explicitly: remove its filters and signal handlers,
    # re-pin its frozen tabs under the new generation, then clear its
    # state so its remaining callbacks and pending timers become no-ops
    # instead of fighting the new generation over the same tabs.
    app = objects.qapp
    app.removeEventFilter(old["expose_filter"])
    app.removeEventFilter(old["resize_filter"])
    try:
        app.focusWindowChanged.disconnect(old["focus_handler"])
    except TypeError:
        pass
    try:
        app.new_window.disconnect(old["wire_window"])
    except TypeError:
        pass
    input_filter = old.get("input_filter")
    if input_filter is not None:
        app.removeEventFilter(input_filter)
    # Newer keys are optional: an old runtime dict (registered by an
    # earlier version of this file) lacks them, and a KeyError here
    # would abort the arm and leave the browser unmanaged with frozen
    # tabs that can never wake.
    hook_conns = old.get("hook_conns")
    if hook_conns is not None:
        # Per-window and per-page signals stay connected to the old
        # generation's slots unless disconnected here; a zombie
        # generation would keep running state passes (and re-freeze tabs
        # the new one just unfroze) after every :config-source.
        for signal, slot in list(hook_conns):
            try:
                signal.disconnect(slot)
            except (TypeError, RuntimeError):
                # The receiver (page or widget) may have been destroyed,
                # taking the signal with it.
                pass
        hook_conns.clear()
    for timer in old["resize_timers"].values():
        timer.stop()
    state_timer = old["state_timer"]
    state_timer.stop()
    try:
        # Kill the old generation's pass path outright: even with its
        # state cleared, untracked signal connections (from generations
        # predating the connection log) would restart this timer and run
        # the old pass logic against live pages.
        state_timer.timeout.disconnect()
    except (TypeError, RuntimeError):
        pass
    for widget_id, label in list(old["overlays"].items()):
        if sip.isdeleted(label):
            continue
        widget = label.parentWidget()
        preview = None
        if widget is not None and not sip.isdeleted(widget):
            _capture_preview(widget_id, widget)
            preview = _previews.get(widget_id)
            if preview is None or preview.isNull():
                preview = old["previews"].get(widget_id)
        if preview is not None and not preview.isNull():
            _show_overlay(widget, preview)
        label.deleteLater()
    for name in (
        "overlays", "previews", "active_since", "resize_timers",
        "resize_polls", "tab_widgets", "loading_pages", "hooked",
        "load_hooked", "frozen_seen", "capture_ok", "win_sizes",
        "input_seen", "unfocused_since",
    ):
        state = old.get(name)
        if state is not None:
            state.clear()


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            old = objreg.get("tabfreeze-runtime", default=None)
            if old is not None:
                _retire(old)
            global _state_timer
            state_timer = QTimer(objects.qapp)
            state_timer.setSingleShot(True)
            state_timer.setInterval(30)
            state_timer.timeout.connect(_apply_state)
            _state_timer = state_timer
            objreg.register(
                "tabfreeze-runtime",
                {
                    "overlays": _overlays,
                    "previews": _previews,
                    "active_since": _active_since,
                    "resize_timers": _resize_timers,
                    "resize_polls": _resize_polls,
                    "tab_widgets": _tab_widgets,
                    "frozen_seen": _frozen_seen,
                    "hooked": _hooked,
                    "load_hooked": _load_hooked,
                    "loading_pages": _loading_pages,
                    "capture_ok": _capture_ok,
                    "state_timer": state_timer,
                    "win_sizes": _win_sizes,
                    "expose_filter": _expose_filter,
                    "resize_filter": _resize_filter,
                    "input_filter": _input_filter,
                    "input_seen": _input_seen,
                    "unfocused_since": _unfocused_since,
                    "hook_conns": _hook_conns,
                    "focus_handler": _on_focus_changed,
                    "wire_window": _wire_window,
                },
                update=True,
            )
            # Group switches move focus and every new window announces
            # itself, so all state changes arrive as events: no polling.
            # QtWayland reports compositor hide/reveal as QEvent.Expose on
            # the QWindow, which is a separate object from the MainWindow
            # widget, so the filter has to be global on the app.
            objects.qapp.installEventFilter(_expose_filter)
            objects.qapp.installEventFilter(_resize_filter)
            objects.qapp.installEventFilter(_input_filter)
            objects.qapp.new_window.connect(_wire_window)
            objects.qapp.focusWindowChanged.connect(_on_focus_changed)
            for window in objreg.window_registry.values():
                _wire_window(window)
            log.misc.info("tabfreeze: armed")
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
