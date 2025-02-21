from libqtile.config import Key
from libqtile.lazy import lazy

import itertools

from .keymap import keymap
from .keymaps.general import general_keybinds
from .keymaps.layers import focus_visible_window, change_tab_layer
from .keymaps.spawn import spawn_position, spawn_tab
from .group.scratchpads import scratchpad_keys


mod = "mod4"
meta = "mod1"

keys = list(itertools.chain(
    general_keybinds,
    focus_visible_window([meta], range(1, 10), ignore_inactive_tabs_at_levels=range(1, 10)),
    change_tab_layer([mod], range(1, 10), range(1, 10)),
    spawn_position([mod], "x", keymap, "x", position="next"),
    spawn_position([mod], "y", keymap, "y", position="next"),
    spawn_position([mod, "shift"], "x", keymap, "x", position="previous"),
    spawn_position([mod, "shift"], "y", keymap, "y", position="previous"),
    spawn_tab([mod], "t", keymap, new_level=False),
    spawn_tab([mod, "shift"], "t", keymap, new_level=True),
    scratchpad_keys([mod], "p", keymap)
))

keys.extend([Key([mod, "control"], "b", lazy.group['scratchpad'].dropdown_toggle('qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py'))])
