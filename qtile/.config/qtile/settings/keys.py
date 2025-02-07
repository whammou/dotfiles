import itertools

from .keymaps.general import general_keybinds
from .keymaps.layers import focus_visible_window, change_tab_layer

keys = []
mod = "mod4"

keys = list(itertools.chain(
    general_keybinds,
    focus_visible_window(9),
    change_tab_layer(9, 9),
))
