from .keymaps.general import general_keybinds
from .keymaps.motions import focus_visible_window, change_bonsai_tab_layer

keys = []
mod = "mod4"

keys.extend(general_keybinds)
keys.extend(focus_visible_window(9))
keys.extend(change_bonsai_tab_layer(9,9))
