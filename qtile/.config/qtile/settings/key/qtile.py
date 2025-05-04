from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


terminal = guess_terminal()
mod = "mod4"

qtile_keys = [
    # Utilities keybindings
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset current column sizes"),
    Key(
        [mod, "Shift"], "n", lazy.layout.normalize_all(), desc="Reset all window sizes"
    ),
]
