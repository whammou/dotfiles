# floatingbars.py - float the status bar (which hosts the commandline
# inside its stack) over the web view only while the current tab is
# frozen, and keep the stock in-layout bar for live tabs. A frozen tab
# is a static pin, so the bar may cover its bottom edge; a live page
# must stay fully visible and interactive, so the default layout (bar
# pushes the page up) is restored for it. Frozen state is asked of the
# engine directly (tabfreeze's pass-cached frozen set lags the engine's
# async flip to Active after an unfreeze, which carries no signal); the
# completion list and qutebrowser's other overlays already position
# relative to the status bar's geometry, so they follow the floating bar
# natively. qutebrowser re-adds the bar to the layout on
# statusbar.position / downloads.position config changes; those are
# re-synced via the config change hook.
import functools
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt import sip
from qutebrowser.qt.core import QEvent, QMetaObject, QObject, QTimer, Qt, pyqtSlot
from qutebrowser.qt.webenginecore import QWebEnginePage
from qutebrowser.utils import log, objreg

_hooked: set[int] = set()
_filters: dict[int, QObject] = {}
_windows: dict[int, Any] = {}
_modes: dict[int, str] = {}
_config_partials: dict[int, Any] = {}
_stack_conns: dict[int, tuple] = {}


def _current_frozen(window: Any) -> bool:
    # Ask the engine: the flip to Active after an unfreeze is async and
    # carries no signal, so tabfreeze's pass-cached frozen set lags and
    # would keep the bar floating over a live tab.
    try:
        tab = window.tabbed_browser.widget.currentWidget()
        if tab is None:
            return False
        page = tab._widget.page()
        return page.lifecycleState() == QWebEnginePage.LifecycleState.Frozen
    except Exception:
        return False


def _reposition(window: Any) -> None:
    try:
        status = window.status
        if sip.isdeleted(status):
            return
        height = status.sizeHint().height()
        if height <= 0:
            height = status.height()
        if height <= 0:
            return
        if config.val.statusbar.position == "top":
            status.setGeometry(0, 0, window.width(), height)
        else:
            status.setGeometry(
                0, window.height() - height, window.width(), height
            )
        status.raise_()
    except Exception:
        log.misc.exception("floatingbars: reposition failed")


def _restore_layout(window: Any) -> None:
    try:
        status = window.status
        if sip.isdeleted(status):
            return
        vbox = window._vbox
        if vbox.indexOf(status) >= 0:
            return
        # Insert at the position qutebrowser's _add_widgets would have
        # used, so the ordering matches a stock window.
        if config.val.statusbar.position == "top":
            vbox.insertWidget(0, status)
        else:
            vbox.addWidget(status)
    except Exception:
        log.misc.exception("floatingbars: restore layout failed")


def _sync_window(window: Any, wid: int) -> None:
    try:
        if window is None or sip.isdeleted(window):
            return
        frozen = _current_frozen(window)
        mode = _modes.get(wid)
        if frozen and mode != "float":
            window._vbox.removeWidget(window.status)
            _reposition(window)
            _modes[wid] = "float"
        elif not frozen and mode != "layout":
            _restore_layout(window)
            _modes[wid] = "layout"
    except Exception:
        log.misc.exception("floatingbars: sync failed")


def _sync_all() -> None:
    # Freeze transitions also happen outside focus events (load
    # deferral, settle window, wake polls), so a low-rate poll catches
    # them; each tick is a couple of dict lookups per window.
    for wid, window in list(_windows.items()):
        _sync_window(window, wid)


def _stack_changed(window: Any, wid: int) -> None:
    try:
        if _modes.get(wid) == "float":
            _reposition(window)
    except Exception:
        log.misc.exception("floatingbars: stack change failed")


def _refloat(wid: int) -> None:
    _sync_window(_windows.get(wid), wid)


def _on_config_changed(wid: int, option: str) -> None:
    if option not in ("statusbar.position", "downloads.position"):
        return
    # The window's own handler just re-added the bar to the layout;
    # re-sync after it ran.
    QTimer.singleShot(0, lambda: _refloat(wid))


class _WindowFilter(QObject):

    def eventFilter(self, a0: Any, a1: QEvent | None) -> bool:
        if a1 is not None and a1.type() == QEvent.Type.Resize:
            wid = id(a0)
            _sync_window(a0, wid)
            if _modes.get(wid) == "float":
                _reposition(a0)
        return False


def _wire_window(window: Any) -> None:
    try:
        wid = id(window)
        if wid in _hooked:
            return
        _hooked.add(wid)
        _windows[wid] = window
        widget = window.tabbed_browser.widget
        widget.currentChanged.connect(
            lambda _i, w=window, wid=wid: _sync_window(w, wid)
        )
        # The stack swaps between the command input row and the message
        # text row, which differ in height; keep the floating bar sized
        # to the active row.
        stack = window.status._stack
        conn = lambda _i, w=window, wid=wid: _stack_changed(w, wid)  # noqa: E731
        stack.currentChanged.connect(conn)
        _stack_conns[wid] = (stack, conn)
        filt = _WindowFilter()
        window.installEventFilter(filt)
        _filters[wid] = filt
        partial = functools.partial(_on_config_changed, wid)
        config.instance.changed.connect(partial)
        _config_partials[wid] = partial
        window.destroyed.connect(
            lambda _o=None, wid=wid: (
                _windows.pop(wid, None),
                _filters.pop(wid, None),
                _config_partials.pop(wid, None),
                _stack_conns.pop(wid, None),
                _modes.pop(wid, None),
                _hooked.discard(wid),
            )
        )
        _sync_window(window, wid)
        log.misc.debug("floatingbars: window %d wired", window.win_id)
    except Exception:
        log.misc.exception("floatingbars: wiring window failed")


def _retire(old: dict) -> None:
    # :config-source re-execs this file; the previous generation's
    # handlers are still connected, so remove them.
    app = objects.qapp
    try:
        app.new_window.disconnect(old["wire_window"])
    except TypeError:
        pass
    try:
        old["poll"].stop()
    except Exception:
        pass
    for wid, window in list(old["windows"].items()):
        try:
            window.removeEventFilter(old["filters"][wid])
        except Exception:
            pass
    for partial in old["config_partials"].values():
        try:
            config.instance.changed.disconnect(partial)
        except TypeError:
            pass
    for stack, conn in old["stack_conns"].values():
        try:
            stack.currentChanged.disconnect(conn)
        except (TypeError, RuntimeError):
            pass
    for name in ("windows", "filters", "modes", "config_partials",
                 "stack_conns", "hooked"):
        old[name].clear()


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            old = objreg.get("floatingbars-runtime", default=None)
            if old is not None:
                _retire(old)
            poll = QTimer(objects.qapp)
            poll.setInterval(250)
            poll.timeout.connect(_sync_all)
            poll.start()
            objreg.register(
                "floatingbars-runtime",
                {
                    "poll": poll,
                    "windows": _windows,
                    "filters": _filters,
                    "modes": _modes,
                    "config_partials": _config_partials,
                    "stack_conns": _stack_conns,
                    "hooked": _hooked,
                    "wire_window": _wire_window,
                },
                update=True,
            )
            objects.qapp.new_window.connect(_wire_window)
            for window in objreg.window_registry.values():
                _wire_window(window)
            log.misc.debug("floatingbars: armed")
        except Exception:
            log.misc.exception("floatingbars: arm failed")


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
