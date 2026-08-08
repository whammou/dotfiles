# pinnedtitle.py - show the current tab's pinned state in the window title.
# qutebrowser's window.title_format has no pinned placeholder: the config
# validator rejects unknown fields and the format pipeline exposes no pinned
# variable. Patching TabbedBrowser at config-source time would not work either:
# qutebrowser purges sys.modules entries added while sourcing a config file
# (configfiles.saved_sys_properties), so the real mainwindow modules are
# imported fresh afterwards and class patches are silently lost. Like
# tabfreeze.py, this module waits for the app and wires instances via objreg
# and signals instead: a per-window wrapper around MainWindow.setWindowTitle
# prepends PINNED_MARKER whenever the current tab is pinned.
import threading
import time
from typing import Any

from qutebrowser.misc import objects
from qutebrowser.qt.core import QMetaObject, QObject, Qt, pyqtSlot
from qutebrowser.utils import log, objreg

# Marker prepended to the window title while the current tab is pinned.
PINNED_MARKER = "[P] "

# Widget ids already wired; a window can announce itself more than once.
_hooked: set[int] = set()


def _wire_window(window: Any) -> None:
    try:
        tb = window.tabbed_browser
        widget = tb.widget
        wid = id(widget)
        if wid in _hooked:
            return
        _hooked.add(wid)

        win = tb._window()
        orig_set = win.setWindowTitle

        def set_window_title(title: str) -> None:
            idx = widget.currentIndex()
            pinned = idx != -1 and bool(widget.widget(idx).data.pinned)
            orig_set((PINNED_MARKER + title) if pinned else title)

        # Instance attribute shadows the Qt method for this window only; the
        # bound original is kept in the closure.
        win.setWindowTitle = set_window_title

        def on_pinned_changed(_pinned: bool) -> None:
            # Re-render the title through the wrapped setter so the marker
            # appears and disappears with the pin state. Every other title
            # update (tab switch, page title, scroll, audio, load progress)
            # already flows through _update_window_title -> setWindowTitle,
            # so the wrapper keeps the marker correct without extra hooks.
            tb._update_window_title()

        def on_new_tab(tab: Any, _idx: int) -> None:
            tab.pinned_changed.connect(on_pinned_changed)

        for i in range(widget.count()):
            tab = widget.widget(i)
            if tab is not None:
                tab.pinned_changed.connect(on_pinned_changed)
        tb.new_tab.connect(on_new_tab)

        # The title rendered before wiring carries no marker; fix it up.
        tb._update_window_title()
        log.misc.debug("pinnedtitle: wired window %d", window.win_id)
    except Exception:
        log.misc.exception("pinnedtitle: wiring window failed")


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            objects.qapp.new_window.connect(_wire_window)
            for window in objreg.window_registry.values():
                _wire_window(window)
        except Exception:
            log.misc.exception("pinnedtitle: arm failed")


def _wait_for_app() -> None:
    # Daemon thread: at interpreter shutdown the objects module is torn down
    # while this thread may still be polling; any error then is irrelevant
    # (the process is exiting), just stop quietly.
    try:
        while objects.qapp is None:
            time.sleep(0.02)
        QMetaObject.invokeMethod(
            _scheduler, "arm", Qt.ConnectionType.QueuedConnection
        )
    except Exception:
        return


_scheduler = _Scheduler()
threading.Thread(target=_wait_for_app, daemon=True).start()
