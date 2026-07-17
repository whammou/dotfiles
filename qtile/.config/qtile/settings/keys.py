from libqtile.config import Key
from libqtile.lazy import lazy

from .key.qtile import qtile_keys
from .key.functional import functional_keys
from .key.layers import focus_visible_window, change_tab_layer, focus_nth_floating
from .key.windows import windows_keys
from .key.keyd import keyd_compat_keys


mod = "mod4"
meta = "mod1"

keys = (
    qtile_keys
    + functional_keys
    + windows_keys
    + keyd_compat_keys
    + focus_visible_window(
        [mod], range(1, 10), ignore_inactive_tabs_at_levels=range(1, 10)
    )
    + focus_nth_floating([mod, "shift"], range(1, 10))
    + change_tab_layer([mod, "shift"], range(1, 10), range(1, 10))
    + [
        Key([mod], "s", lazy.layout.spawn("wlr-which-key"), desc="Spawn"),
        Key([mod], "f", lazy.layout.spawn_float("wlr-which-key"), desc="Scratchpad (floating)"),
        Key([mod], "v", lazy.layout.spawn_split("wlr-which-key", "x"), desc="Split right"),
        Key([mod], "x", lazy.layout.spawn_split("wlr-which-key", "y"), desc="Split below"),
        Key([mod, "shift"], "v", lazy.layout.spawn_split("wlr-which-key", "x", position="previous"), desc="Split left"),
        Key([mod, "shift"], "x", lazy.layout.spawn_split("wlr-which-key", "y", position="previous"), desc="Split above"),
        Key([mod], "t", lazy.layout.spawn_tab("wlr-which-key"), desc="Tab"),
        Key([mod], "n", lazy.layout.spawn_tab("wlr-which-key", position="next"), desc="Tab next"),
        Key([mod], "p", lazy.layout.spawn_tab("wlr-which-key", position="previous"), desc="Tab prev"),
        Key([mod, "control"], "t", lazy.layout.spawn_tab("wlr-which-key", new_level=True), desc="Tab new level"),
        Key([mod, "control"], "n", lazy.layout.spawn_tab("wlr-which-key", new_level=True, position="next"), desc="Tab new level next"),
        Key([mod, "control"], "p", lazy.layout.spawn_tab("wlr-which-key", new_level=True, position="previous"), desc="Tab new level prev"),
        Key([mod, "shift"], "t", lazy.layout.spawn_tab("wlr-which-key"), desc="Tab shift"),
        Key([mod, "shift"], "n", lazy.layout.spawn_tab("wlr-which-key", position="next"), desc="Tab shift next"),
        Key([mod, "shift"], "p", lazy.layout.spawn_tab("wlr-which-key", position="previous"), desc="Tab shift prev"),
    ]
)
