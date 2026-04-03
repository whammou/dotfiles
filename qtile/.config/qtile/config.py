from libqtile import hook, qtile
from libqtile.backend.wayland.inputs import InputConfig

from settings.keys import mod, keys
from settings.groups import groups
from settings.layouts import layouts, floating_layout
from settings.widgets import widget_defaults, extension_defaults
from settings.screens import screens
from settings.mouse import mouse
from settings.path import qtile_path

from os import path
import subprocess


@hook.subscribe.startup_once
def autostart():
    subprocess.call([path.join(qtile_path, "autostart.sh")])


@hook.subscribe.unlocked
@hook.subscribe.startup
def session_start():
    qtile.spawn("systemctl --user start qtile-session.target")
    qtile.spawn("systemctl --user restart screensaver")


@hook.subscribe.shutdown
@hook.subscribe.locked
def session_lock():
    qtile.spawn("systemctl --user stop qtile-session.target")


wl_input_rules = {
    "TPPS/2 IBM TrackPoint": InputConfig(events=False, dwt=True, left_handed=True),
    "*": InputConfig(
        left_handed=False,
        pointer_accel=False,
        send_events=False,
        tap=False,
        dwt=True,
        events=False,
    ),
    "type:keyboard": InputConfig(kb_options="ctrl:nocaps,compose:ralt"),
}

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = False
cursor_warp = False
auto_fullscreen = False
focus_on_window_activation = "never"
focus_previous_on_window_remove = True
reconfigure_screens = True
auto_minimize = True
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"
