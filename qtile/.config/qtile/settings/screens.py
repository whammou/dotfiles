from libqtile.config import Screen
from libqtile import bar
from libqtile import widget

from .widgets import widgets
from .path import wallpaper_path

from os import path


def status_bar(widgets, **kargs):
    return bar.Bar(widgets, 26, **kargs)

def select_wallpaper(wallpaper):
    wallpaper = path.join(wallpaper_path, wallpaper)
    return wallpaper


screens = [Screen(
    wallpaper = select_wallpaper("meteor.jpg"),
    wallpaper_mode = "fill",
    top = status_bar(widgets, margin=[6, 12, 12, 12]),
    left = bar.Bar([], 6),
    right = bar.Bar([], 1)
)]
