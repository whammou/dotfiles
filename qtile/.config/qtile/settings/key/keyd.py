"""Arrow-key variants of hjkl window operations for keyd vimmode compatibility.

When keyd's vimmode layer is active, h/j/k/l are intercepted and converted
to Left/Right/Up/Down arrow keys before they reach the compositor.  This
breaks any qtile binding that expects the raw letter keys (e.g. M-S-h for
swap-left).

This module provides the same window operations bound to their corresponding
arrow keys.  Because keyd forwards all keystrokes (including unbound modifier
keys) through its single uinput device, the modifier state from the physical
keyboard is preserved on the same device, so qtile sees e.g. Mod4+Shift+Left
and matches these bindings.

Maintain alongside the hjkl originals in windows.py — keep both sets so
operations work whether vimmode is ON (arrow keys) or OFF (letter keys).
"""

from libqtile.config import EzKey
from libqtile.lazy import lazy


keyd_compat_keys = [
    # Move floating — M-arrows (hjkl originals in windows.py)
    EzKey("M-<Left>", lazy.window.move_floating(-32, 0).when(when_floating=True)),
    EzKey("M-<Right>", lazy.window.move_floating(+32, 0).when(when_floating=True)),
    EzKey("M-<Up>", lazy.window.move_floating(0, -18).when(when_floating=True)),
    EzKey("M-<Down>", lazy.window.move_floating(0, +18).when(when_floating=True)),
    # Resize — M-C-arrows (hjkl originals in windows.py)
    EzKey("M-C-<Left>", lazy.layout.resize("left", 300)),
    EzKey("M-C-<Right>", lazy.layout.resize("right", 300)),
    EzKey("M-C-<Up>", lazy.layout.resize("up", 300)),
    EzKey("M-C-<Down>", lazy.layout.resize("down", 300)),
    # Swap — M-S-arrows (hjkl originals in windows.py)
    EzKey("M-S-<Left>", lazy.layout.swap("left")),
    EzKey("M-S-<Right>", lazy.layout.swap("right")),
    EzKey("M-S-<Up>", lazy.layout.swap("up")),
    EzKey("M-S-<Down>", lazy.layout.swap("down")),
]
