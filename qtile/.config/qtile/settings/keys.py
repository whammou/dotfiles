import itertools

from .keymaps import keymap
from .key.qtile import qtile_keys
from .key.functional import functional_keys
from .key.layers import focus_visible_window, change_tab_layer
from .key.windows import windows_keys
from .key.spawn import spawn_position, spawn_tab
from .group.scratchpads import scratchpad_keys


mod = "mod4"
meta = "mod1"

keys = list(
    itertools.chain(
        qtile_keys,
        functional_keys,
        windows_keys,
        focus_visible_window(
            [meta], range(1, 10), ignore_inactive_tabs_at_levels=range(1, 10)
        ),
        change_tab_layer([mod], range(1, 10), range(1, 10)),
        spawn_position([mod], "x", keymap, "x", position="next"),
        spawn_position([mod], "y", keymap, "y", position="next"),
        spawn_position([mod, "shift"], "x", keymap, "x", position="previous"),
        spawn_position([mod, "shift"], "y", keymap, "y", position="previous"),
        spawn_tab([mod], "t", keymap, new_level=False),
        spawn_tab([mod, "shift"], "t", keymap, new_level=True),
        scratchpad_keys([mod], "p", keymap),
    )
)
