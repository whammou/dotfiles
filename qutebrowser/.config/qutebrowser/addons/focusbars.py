# focusbars.py - show the status bar (which hosts the commandline inside
# its stack) only in the focused window, and keep it hidden in every
# unfocused one. tabfreeze keeps some unfocused tabs live (media,
# capture, pinned, exempt domains), so "frozen or not" is the wrong
# test: window focus is the single rule. The focused window's bar is
# left to the bar's own maybe_hide(), which re-applies the
# statusbar.show strategy.
import functools
import threading
import time
from typing import Any

from qutebrowser.config import config
from qutebrowser.misc import objects
from qutebrowser.qt import sip
from qutebrowser.qt.core import QMetaObject, QObject, QTimer, Qt, pyqtSlot
from qutebrowser.utils import log, objreg

_hooked: set[int] = set()
_windows: dict[int, Any] = {}
_modes: dict[int, str] = {}
_config_partials: dict[int, Any] = {}


def _window_focused(window: Any) -> bool:
    # The same focus test tabfreeze uses: the window receiving key
    # events is the active one; when the whole app loses focus none is.
    try:
        handle = window.windowHandle()
        return handle is not None and handle.isActive()
    except Exception:
        return False


def _sync_window(window: Any, wid: int) -> None:
    try:
        if window is None or sip.isdeleted(window):
            return
        status = window.status
        if sip.isdeleted(status):
            return
        if not _window_focused(window):
            # Asserted on every tick, not just on transitions: the show
            # strategy is a global config, so e.g. "o" in another window
            # re-shows this bar between ticks.
            status.hide()
            _modes[wid] = "hidden"
        elif _modes.get(wid) != "shown":
            # qutebrowser's own predicate re-applies statusbar.show and
            # fullscreen handling in the focused window.
            status.maybe_hide()
            _modes[wid] = "shown"
    except Exception:
        log.misc.exception("focusbars: sync failed")


def _sync_all() -> None:
    for wid, window in list(_windows.items()):
        _sync_window(window, wid)


def _on_config_changed(wid: int, option: str) -> None:
    if option != "statusbar.show":
        return
    _sync_window(_windows.get(wid), wid)


def _wire_window(window: Any) -> None:
    try:
        wid = id(window)
        if wid in _hooked:
            return
        _hooked.add(wid)
        _windows[wid] = window
        partial = functools.partial(_on_config_changed, wid)
        config.instance.changed.connect(partial)
        _config_partials[wid] = partial
        window.destroyed.connect(
            lambda _o=None, wid=wid: (
                _windows.pop(wid, None),
                _config_partials.pop(wid, None),
                _modes.pop(wid, None),
                _hooked.discard(wid),
            )
        )
        _sync_window(window, wid)
        log.misc.debug("focusbars: window %d wired", window.win_id)
    except Exception:
        log.misc.exception("focusbars: wiring window failed")


def _retire(old: dict) -> None:
    # :config-source re-execs this file; the previous generation's
    # handlers are still connected, so remove them.
    try:
        objects.qapp.new_window.disconnect(old["wire_window"])
    except TypeError:
        pass
    try:
        objects.qapp.focusWindowChanged.disconnect(old["focus_handler"])
    except TypeError:
        pass
    try:
        old["poll"].stop()
    except Exception:
        pass
    for partial in old["config_partials"].values():
        try:
            config.instance.changed.disconnect(partial)
        except TypeError:
            pass
    for name in ("windows", "config_partials", "modes", "hooked"):
        old[name].clear()


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            old = objreg.get("focusbars-runtime", default=None)
            if old is not None:
                _retire(old)
            # One-time orphan cleanup: the previous generations lived
            # under the old "floatingbars"/"frozenbars" names and never
            # get retired by the new one, so stop them here.
            for legacy_name in ("floatingbars-runtime", "frozenbars-runtime"):
                legacy = objreg.get(legacy_name, default=None)
                if legacy is not None:
                    _retire(legacy)
                    try:
                        objreg.delete(legacy_name)
                    except Exception:
                        pass
            poll = QTimer(objects.qapp)
            poll.setInterval(250)
            poll.timeout.connect(_sync_all)
            poll.start()
            focus_handler = lambda _w=None: _sync_all()  # noqa: E731
            objreg.register(
                "focusbars-runtime",
                {
                    "poll": poll,
                    "focus_handler": focus_handler,
                    "windows": _windows,
                    "config_partials": _config_partials,
                    "modes": _modes,
                    "hooked": _hooked,
                    "wire_window": _wire_window,
                },
                update=True,
            )
            objects.qapp.new_window.connect(_wire_window)
            objects.qapp.focusWindowChanged.connect(focus_handler)
            for window in objreg.window_registry.values():
                _wire_window(window)
            log.misc.debug("focusbars: armed")
        except Exception:
            log.misc.exception("focusbars: arm failed")


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
