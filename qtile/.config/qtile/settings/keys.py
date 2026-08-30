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
        Key([mod], "space", lazy.layout.spawn("wlr-which-key"), desc="Spawn"),
    ]
)
