import itertools

from libqtile.config import Key
from libqtile.lazy import lazy

from .keymaps import keymap
from .key.qtile import qtile_keys
from .key.functional import functional_keys
from .key.layers import focus_visible_window, change_tab_layer, focus_nth_floating
from .key.windows import windows_keys
from .key.spawn import spawn_position, spawn_new, spawn_tab
from .group.scratchpads import scratchpad_keys
from .which_key import show_which_key


mod = "mod4"
meta = "mod1"

keys = list(
    itertools.chain(
        qtile_keys,
        functional_keys,
        windows_keys,
        focus_visible_window(
            [mod], range(1, 10), ignore_inactive_tabs_at_levels=range(1, 10)
        ),
        focus_nth_floating([mod, "shift"], range(1, 10)),
        change_tab_layer([mod, "shift"], range(1, 10), range(1, 10)),
        spawn_new([mod], "s", keymap),
        scratchpad_keys([mod], "f", keymap),
        spawn_position([mod], "v", keymap, "x", position="next"),
        spawn_position([mod], "x", keymap, "y", position="next"),
        spawn_position([mod, "shift"], "v", keymap, "x", position="previous"),
        spawn_position([mod, "shift"], "x", keymap, "y", position="previous"),
        spawn_tab([mod], "t", keymap, new_level=False, level=1),
        spawn_tab([mod], "n", keymap, new_level=False, level=1, position="next"),
        spawn_tab([mod], "p", keymap, new_level=False, level=1, position="previous"),
        spawn_tab([mod, "control"], "t", keymap, new_level=True),
        spawn_tab([mod, "control"], "n", keymap, new_level=True, position="next"),
        spawn_tab([mod, "control"], "p", keymap, new_level=True, position="previous"),
        spawn_tab([mod, "shift"], "t", keymap, new_level=False),
        spawn_tab([mod, "shift"], "n", keymap, new_level=False, position="next"),
        spawn_tab([mod, "shift"], "p", keymap, new_level=False, position="next"),
        [
            Key(
                [mod],
                "slash",
                lazy.function(show_which_key),
                desc="Show which-key overlay",
            )
        ],
    )
)
