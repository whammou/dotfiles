import itertools

from .keymaps.keymap import cmd_keymaps
from .keymaps.general import general_keybinds
from .keymaps.layers import focus_visible_window, change_tab_layer
from .keymaps.spawn import spawn_position, spawn_tab

keys = []
mod = "mod4"

keys = list(itertools.chain(
    general_keybinds,
    focus_visible_window(range(1, 10)),
    change_tab_layer(range(1, 10), range(1, 10)),
    spawn_position(cmd_keymaps, "x", "next"),
    spawn_position(cmd_keymaps, "y", "next"),
    spawn_position(cmd_keymaps, "x", "previous"),
    spawn_position(cmd_keymaps, "y", "previous"),
    spawn_tab(cmd_keymaps),
    spawn_tab(cmd_keymaps, newlevel=True),
))
