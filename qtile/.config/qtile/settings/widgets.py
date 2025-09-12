from libqtile import bar
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_bonsai import BonsaiBar

from .theme import colors
from .widget.floating_count import FloatCount


def base(fg="text", bg="bg2"):
    return {"foreground": colors[fg], "background": colors[bg]}


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def icon(fg="text", bg="bg2", fontsize=16, text="?"):
    return widget.TextBox(**base(fg, bg), fontsize=fontsize, text=text, padding=3)


def workspaces():
    return [
        BonsaiBar(
            **{
                "tab.bg_color": colors["blue_dimmed"],
                "tab.fg_color": colors["bg2"],
                "tab.active.bg_color": colors["blue"],
                "tab.active.fg_color": colors["bg2"],
                "length": bar.CALCULATED,
                "font_size": 16,
                "tab.padding": [0, 5, 10, 5],
            }
        ),
        separator(),
        widget.TextBox(**base(fg="blue"), fmt=" []="),
        widget.Prompt(
            **base(fg="blue"),
            font="Sauce Code Pro Nerd Medium",
            cursor=False,
            fmt="{}",
            prompt="",
        ),
        separator(),
        widget.WindowName(
            **base(fg="fg"),
            font="Sauce Code Pro Nerd Font Medium",
            fontsize=15,
            padding=5,
        ),
        separator(),
    ]


def checkupdate(command="checkupdates"):
    return widget.CheckUpdates(
        background=colors["bg2"],
        colour_have_updates=colors["yellow"],
        colour_no_updates=colors["yellow"],
        display_format="  PKGS: {updates} ",
        no_update_string="  PKGS: 0 ",
        update_interval=1800,
        custom_command=command,
    )


def battery(bat):
    return widget.Battery(
        **base(fg="green"),
        battery=bat,
        discharge_char="󰁿",
        not_charging_char="󱧥",
        charge_char="",
        full_char="󰁹",
        empty_char="󱟩",
        format="{char} {percent:2.0%} ",
        show_short_text=False,
        low_percentage=0.05,
        low_foreground=colors["red"],
        notify_below=0.05,
        update_interval=60,
    )


def disk_free():
    return widget.DF(
        **base(fg="red"),
        partition="/home",
        format="{uf}{m}",
        # format = "{r: 0.0f}",
        fmt=" FREE: {}  ",
        visible_on_warn=False,
        update_interval=600,
    )


def net():
    return widget.Net(
        **base(bg="bg2", fg="blue"),
        interface="wlan0",
        format="  {down:03.0f}{down_suffix:<2}  {up:03.0f}{up_suffix:<2} ",
        prefix="k",
        update_interval=60,
    )


def wlan():
    return widget.Wlan(
        **base(bg="bg2", fg="purple"),
        format=" 󰤨 STRG: {percent:2.0%} ",
        update_interval=60,
    )


powerline = {"decorations": [PowerLineDecoration(path="arrow_right")]}

widgets = [
    *workspaces(),
    widget.Sep(**base(bg="bg2", fg="bg2"), linewidth=16),
    disk_free(),
    battery(0),
    battery(1),
    checkupdate(),
    FloatCount(**base(bg="bg2", fg="blue"), format="  FLTW: {count} "),
    # net(),
    wlan(),
    widget.Clock(**base(bg="bg2", fg="cyan"), format="%d/%m/%Y - %H:%M", fmt=" 󰸘 {} "),
    # widget.Systray(background=colors["bg2"], padding=10, icon_size=20),
    # widget.Sep(**base(bg="bg2", fg="bg2"), linewidth=8),
    widget.TextBox(**base(bg="bg2", fg="fg"), text="󰤳 "),
    widget.TextBox(**base(bg="bg2", fg="fg"), text=""),
    widget.TextBox(**base(bg="bg2", fg="fg"), text=""),
    widget.TextBox(**base(bg="bg2", fg="fg"), text=""),
    widget.TextBox(**base(bg="bg2", fg="fg"), text=""),
    widget.Sep(background=colors["bg2"], foreground=colors["bg2"], linewidth=2),
]

widget_defaults = dict(
    font="Sauce Code Pro Nerd Font Bold",
    fontsize=16,
    padding=3,
)

extension_defaults = widget_defaults.copy()
