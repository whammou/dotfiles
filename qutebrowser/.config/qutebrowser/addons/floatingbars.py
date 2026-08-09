# floatingbars.py - float the status bar (which hosts the commandline
# inside its stack) over the web view instead of pushing it down in the
# window layout, so showing/hiding the commandline or status bar never
# resizes the page. The completion list and qutebrowser's other overlays
# already position relative to the status bar's geometry, so they follow
# the floating bar natively. qutebrowser re-adds the bar to the layout
# on statusbar.position / downloads.position config changes; those are
# re-floated via the config change hook.
import functools
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt import sip
from qutebrowser.qt.core import QEvent, QMetaObject, QObject, QTimer, Qt, pyqtSlot
from qutebrowser.utils import log, objreg

_hooked: set[int] = set()
_filters: dict[int, QObject] = {}
_windows: dict[int, Any] = {}
_config_partials: dict[int, Any] = {}
_stack_conns: dict[int, tuple] = {}


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


def _refloat(wid: int) -> None:
    try:
        window = _windows.get(wid)
        if window is None or sip.isdeleted(window):
            return
        window._vbox.removeWidget(window.status)
        _reposition(window)
    except Exception:
        log.misc.exception("floatingbars: re-float failed")


def _on_config_changed(wid: int, option: str) -> None:
    if option not in ("statusbar.position", "downloads.position"):
        return
    # The window's own handler just re-added the bar to the layout;
    # re-float after it ran.
    QTimer.singleShot(0, lambda: _refloat(wid))


class _WindowFilter(QObject):

    def eventFilter(self, a0: Any, a1: QEvent | None) -> bool:
        if a1 is not None and a1.type() == QEvent.Type.Resize:
            _reposition(a0)
        return False


def _wire_window(window: Any) -> None:
    try:
        wid = id(window)
        if wid in _hooked:
            return
        _hooked.add(wid)
        _windows[wid] = window
        window._vbox.removeWidget(window.status)
        _reposition(window)
        # The stack swaps between the command input row and the message
        # text row, which differ in height; keep the bar sized to the
        # active row.
        stack = window.status._stack
        conn = lambda _i, w=window: _reposition(w)  # noqa: E731
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
                _hooked.discard(wid),
            )
        )
        log.misc.debug("floatingbars: window %d floated", window.win_id)
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


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            old = objreg.get("floatingbars-runtime", default=None)
            if old is not None:
                _retire(old)
            objreg.register(
                "floatingbars-runtime",
                {
                    "windows": _windows,
                    "filters": _filters,
                    "config_partials": _config_partials,
                    "stack_conns": _stack_conns,
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
