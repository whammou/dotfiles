from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy


mod = "mod4"
alt = "mod1"

functional_keys = [
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("volume toggle"),
    ),
    Key([], "XF86AudioLowerVolume", lazy.spawn("volume 1%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("volume 1%+")),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute 0 toggle")),
    Key(["Shift"], "XF86AudioMicMute", lazy.spawn("noise-supression")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightness 1%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightness 1%+")),
    Key([], "XF86Display", lazy.group["scratchpad"].dropdown_toggle("a2ln")),
    Key([], "F8", lazy.group["scratchpad"].dropdown_toggle("nmfzf")),
    # Key(["Control"], "F8", lazy.group["scratchpad"].dropdown_toggle("a2ln")),
    Key([], "XF86Tools", lazy.spawn("rofi-mount")),
    Key([], "XF86Search", lazy.spawn("rofi-playerctl")),
    Key([], "XF86LaunchA", lazy.spawn("vktablet")),
    Key([], "XF86Explorer", lazy.spawn("adapter-switch")),
    Key([mod], "Print", lazy.spawn("flameshot screen")),
    Key([mod, "Shift"], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "Space", lazy.spawn("toggle-trackpoint")),
    Key([mod, "Shift"], "Space", lazy.spawn("_keyboard_toggle")),
    Key(
        [mod],
        "Delete",
        lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu"),
    ),
    Key([mod], "Home", lazy.spawn("dunstctl history-pop")),
    Key([mod, "Shift"], "Home", lazy.spawn("dunstctl context")),
    Key([mod], "End", lazy.spawn("dunstctl close")),
    Key([mod, "Control"], "End", lazy.spawn("dunstctl history-clear")),
    Key([mod, "Shift"], "End", lazy.spawn("dunstctl close-all")),
    Key(
        [alt, "Control"],
        "v",
        lazy.spawn("_cliphist-list"),
    ),
]
