"""Arrow-key and Shift-arrow variants of hjkl window operations for keyd
vimmode and visual mode compatibility.

Vimmode:  h/j/k/l → Left/Down/Up/Right (bare arrows, no modifier baked in)
Visual mode:  h/j/k/l → S-left/S-down/S-up/S-right (Shift+arrows, Shift baked in)

This breaks qtile bindings that expect the raw letter keys (e.g. M-S-h for
swap-left).  This module provides the same window operations bound to their
corresponding arrow keys.  Because keyd forwards all keystrokes (including
unbound modifier keys) through its single uinput device, the modifier state
from the physical keyboard is preserved on the same device, so qtile sees e.g.
Mod4+Shift+Left and matches these bindings.

Vimmode complement (bare arrows):
  - meta+h → Left    → EzKey("M-<Left>")       — move floating
  - meta+ctrl+h → Left → EzKey("M-C-<Left>")   — resize
  - meta+shift+h → Left → EzKey("M-S-<Left>")  — swap

Visual mode complement (Shift+arrows, from `visual.h = S-left` etc.):
  - meta+shift+h → S-left → EzKey("M-S-<Left>")    — swap    (same as vimmode)
  - meta+ctrl+h  → S-left → EzKey("M-C-S-<Left>")  — resize  (+Shift vs vimmode)

Letter-key passthroughs in app.conf (meta+visual.h = macro(h)) bypass the
S- transformation so meta+h still reaches the original M-h move bindings
when meta is held.

Maintain alongside the hjkl originals in windows.py — keep both sets so
operations work whether vimmode/visual is ON (arrow/shift-arrow keys) or OFF
(letter keys).
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
    # Covers both: vimmode meta+shift+h → Left → M-S-Left (via vimmode.h = left)
    #               visual meta+shift+h → S-left → M-S-Left (via visual.h = S-left)
    EzKey("M-S-<Left>", lazy.layout.swap("left")),
    EzKey("M-S-<Right>", lazy.layout.swap("right")),
    EzKey("M-S-<Up>", lazy.layout.swap("up")),
    EzKey("M-S-<Down>", lazy.layout.swap("down")),
    # Visual mode resize — M-C-S-arrows (visual.h = S-{left,right,up,down})
    # Vimmode uses M-C-arrows (bare arrows, no shift); visual adds Shift from S-
    EzKey("M-C-S-<Left>", lazy.layout.resize("left", 300)),
    EzKey("M-C-S-<Right>", lazy.layout.resize("right", 300)),
    EzKey("M-C-S-<Up>", lazy.layout.resize("up", 300)),
    EzKey("M-C-S-<Down>", lazy.layout.resize("down", 300)),
]
