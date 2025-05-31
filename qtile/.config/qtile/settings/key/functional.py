from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy


mod = "mod4"
alt = "mod1"

functional_keys = [
    Key(
        [alt],
        "F1",
        lazy.spawn(
            "pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle"
        ),
    ),
    Key([alt], "F2", lazy.spawn("volume 1%-")),
    Key([alt], "F3", lazy.spawn("volume 1%+")),
    Key([alt], "F4", lazy.spawn("pactl set-source-mute 0 toggle")),
    Key([alt, "Shift"], "F4", lazy.spawn("noise-supression")),
    Key([alt], "F5", lazy.spawn("brightness 1%-")),
    Key([alt], "F6", lazy.spawn("brightness 1%+")),
    Key([alt], "F7", lazy.spawn("uptime-notification")),
    Key([alt], "F8", lazy.group["scratchpad"].dropdown_toggle("nmfzf")),
    Key([alt, "Shift"], "F8", lazy.group["scratchpad"].dropdown_toggle("a2ln")),
    Key([alt], "F9", lazy.group["scratchpad"].dropdown_toggle("samba")),
    Key([alt], "F10", lazy.group["scratchpad"].dropdown_toggle("calendar")),
    Key([alt], "F11", lazy.spawn("vktablet")),
    Key([alt], "F12", lazy.group["scratchpad"].dropdown_toggle("adapter")),
    Key([mod], "Space", lazy.spawn("sh /usr/local/bin/toggle-trackpoint")),
    # Key([alt], "Delete", lazy.group["scratchpad"].dropdown_toggle("powermenu")),
    Key(
        [alt],
        "Delete",
        lazy.spawn("rofi -show power-menu -modi power-menu:/sbin/rofi-power-menu"),
    ),
    Key([alt], "Escape", lazy.spawn("dunstctl close")),
    Key([alt, "Shift"], "Escape", lazy.spawn("dunstctl close-all")),
    Key(
        [alt, "Control"],
        "v",
        lazy.spawn(
            "rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'"
        ),
    ),
    KeyChord(
        [mod, "shift"],
        "s",
        [
            Key([], "s", lazy.spawn("flameshot screen")),
            Key([], "c", lazy.spawn("flameshot gui")),
        ],
    ),
]
