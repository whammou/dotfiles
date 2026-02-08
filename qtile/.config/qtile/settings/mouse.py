from libqtile.config import Drag, Click
from libqtile.lazy import lazy
from .keys import mod

mouse = [
    Click([], "Button2", lazy.spawn("_keyboard_toggle")),
]
