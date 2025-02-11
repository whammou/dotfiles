import itertools

from .keymap import keymap
from .keymaps.general import general_keybinds
from .keymaps.layers import focus_visible_window, change_tab_layer
from .keymaps.spawn import spawn_position, spawn_tab

keys = []
mod = "mod4"

keys = list(itertools.chain(
    general_keybinds,
    focus_visible_window(range(1, 10)),
    change_tab_layer(range(1, 10), range(1, 10)),
    spawn_position(keymap, "x", "next"),
    spawn_position(keymap, "y", "next"),
    spawn_position(keymap, "x", "previous"),
    spawn_position(keymap, "y", "previous"),
    spawn_tab(keymap),
    spawn_tab(keymap, newlevel=True),
))
