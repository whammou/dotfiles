from libqtile import hook, qtile
from libqtile.backend.wayland.inputs import InputConfig
import logging
from libqtile.log_utils import logger


from settings.keys import mod, keys
from settings.groups import groups
from settings.layouts import layouts, floating_layout
from settings.widgets import widget_defaults, extension_defaults
from settings.screens import screens
from settings.mouse import mouse
from settings.path import qtile_path

from os import path

# Set the log level to CRITICAL to stop regular logs
logger.setLevel(logging.CRITICAL)


@hook.subscribe.startup_once
def autostart():
    qtile.spawn([path.join(qtile_path, "autostart.sh")])


# Lock state: qtile-lock.target mirrors lock/unlock.
#   locked   -> systemctl --user start qtile-lock.target
#   unlocked -> systemctl --user stop qtile-lock.target
# Session services (qtile-session.target wants) declare
# Conflicts=qtile-lock.target, so they pause while locked and are restarted
# by `start qtile-session.target` on unlock.
# qtile.service's PartOf=qtile-session.target is cleared via
# qtile.service.d/lifecycle.conf, so locking never stops the compositor.


@hook.subscribe.locked
def session_lock():
    qtile.spawn("systemctl --user stop qtile-unlock.target")


@hook.subscribe.unlocked
@hook.subscribe.startup
def session_unlock():
    qtile.spawn("systemctl --user start qtile-unlock.target")
    qtile.spawn("systemctl --user restart screensaver")


wl_input_rules = {
    # Disable accel for every pointer: flat profile + speed 0 = no accel (libinput)
    # Verified via get_inputs 2026-08-28 — TrackPoint is 2:10:TPPS/2 IBM TrackPoint
    "2:10:TPPS/2 IBM TrackPoint": InputConfig(
        dwt=True, left_handed=True, pointer_accel=0.5, accel_profile="flat"
    ),
    "*": InputConfig(
        left_handed=False,
        pointer_accel=0,
        accel_profile="flat",
        tap=False,
        dwt=True,
    ),
    "type:keyboard": InputConfig(
        kb_layout="qtile-ralt-nav",
        kb_options="caps:swapescape",
    ),
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
