from libqtile.config import Screen
from libqtile import bar

from .widgets import widgets
from .path import wallpaper_path

from os import path


GAP = 1
OFFSET = 1


def status_bar(widgets, **kargs):
    return bar.Bar(widgets, 28, **kargs)


def select_wallpaper(wallpaper):
    wallpaper = path.join(wallpaper_path, wallpaper)
    return wallpaper


screens = [
    Screen(
        wallpaper=select_wallpaper("Waves Light 6016x6016.jpg"),
        wallpaper_mode="fill",
        top=status_bar(
            widgets,
            margin=[
                GAP * 4,  # TOP
                GAP * 4,  # RIGHT
                GAP * 4,  # BOTTOM
                GAP * 4,  # LEFT
            ],
        ),
        right=bar.Bar(
            [],
            1,
            margin=[0, int(-OFFSET), 0, GAP + OFFSET],
        ),
        left=bar.Bar([], 1, margin=[0, GAP + OFFSET, 0, int(-OFFSET)]),
    )
]
