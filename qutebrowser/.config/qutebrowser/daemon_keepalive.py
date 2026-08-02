# monkey-patch: prevent daemon exit when last window closes
import sys as _sys
if '--nowindow' in _sys.argv:
    import qutebrowser.misc.quitter as _q
    _q.Quitter.on_last_window_closed = lambda self: None
