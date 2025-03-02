from libqtile.config import Key
from libqtile.lazy import lazy


mod = "mod4"

functional_keys = [
    Key(
        [mod],
        "F1",
        lazy.spawn(
            "pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle"
        ),
    ),
    Key([mod], "F2", lazy.spawn("dec-volume-notification")),
    Key([mod], "F3", lazy.spawn("inc-volume-notification")),
    Key([mod], "F4", lazy.spawn("pactl set-source-mute 0 toggle")),
    Key([mod, "Shift"], "F4", lazy.spawn("noise-supression")),
    Key([mod], "F5", lazy.spawn("brightnessctl set 5%-")),
    Key([mod], "F6", lazy.spawn("brightnessctl set +5%")),
    Key([mod], "F7", lazy.spawn("uptime-notification")),
    Key([mod], "F8", lazy.group["scratchpad"].dropdown_toggle("nmfzf")),
    Key([mod], "F11", lazy.spawn("vktablet")),
    Key([mod], "F12", lazy.group["scratchpad"].dropdown_toggle("adapter")),
    Key([mod], "Space", lazy.spawn("sh /usr/local/bin/toggle-trackpoint")),
]
