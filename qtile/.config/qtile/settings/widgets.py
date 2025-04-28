from libqtile import bar
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_bonsai import BonsaiBar

from .theme import colors


def base(fg="text", bg="bg0"):
    return {"foreground": colors[fg], "background": colors[bg], **powerline}


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def text_separator():
    return widget.TextBox(**base(fg="fg"), fmt="")


def icon(fg="text", bg="bg0", fontsize=16, text="?"):
    return widget.TextBox(**base(fg, bg), fontsize=fontsize, text=text, padding=3)


def workspaces():
    return [
        BonsaiBar(
            **{
                "tab.bg_color": colors["bg0"],
                "tab.fg_color": colors["grey"],
                "tab.active.fg_color": colors["blue"],
                "tab.active.bg_color": colors["bg1"],
                "length": bar.CALCULATED,
                "font_size": 16,
                "tab.padding": [-5, 10, 10, 10],
            }
        ),
        separator(),
        widget.TextBox(**base(fg="blue"), fmt="[]="),
        widget.Prompt(**base(fg="blue"), cursor=False, fmt="{}", prompt=""),
        separator(),
        widget.WindowName(**base(fg="fg"), fontsize=15, padding=5),
        separator(),
    ]


def checkupdate(command="checkupdates"):
    return widget.CheckUpdates(
        background=colors["green"],
        colour_have_updates=colors["text"],
        colour_no_updates=colors["text"],
        no_update_string="0",
        display_format="{updates} ",
        update_interval=1800,
        custom_command=command,
        **powerline,
    )


def battery(bat):
    return widget.Battery(
        **base(fg="green"),
        battery=bat,
        discharge_char="󰁿 ",
        not_charging_char="󱧥 ",
        charge_char=" ",
        full_char="󰁹 ",
        empty_char="󱟩 ",
        format="{char}{percent:2.0%}",
        show_short_text=False,
        low_percentage=0.05,
        low_foreground=colors["red"],
        notify_below=0.05,
        update_interval=60,
    )


def disk_free():
    return widget.DF(
        **base(fg="purple"),
        partition="/",
        format="{uf}{m}",
        # format = "{r: 0.0f}",
        fmt=" {}",
        visible_on_warn=False,
        update_interval=600,
    )


def net():
    return widget.Net(
        **base(bg="blue"),
        interface="wlan0",
        format=" {down:6.1f}{down_suffix:<2} {up:6.1f}{up_suffix:<2}",
        update_interval=60,
    )


def wlan():
    return widget.Wlan(
        **base(bg="red"),
        format="{percent:2.0%} ",
        update_interval=60,
    )


powerline = {"decorations": [PowerLineDecoration(path="arrow_right")]}

widgets = [
    *workspaces(),
    disk_free(),
    text_separator(),
    battery(0),
    battery(1),
    separator(),
    icon(bg="green", text=" "),  # Icon: nf-fa-download
    checkupdate(),
    net(),
    # widget.CurrentLayout(**base(bg='red'), padding=5),
    icon(bg="red", text=" 󰤨"),  # Icon: nf-fa-feed
    wlan(),
    icon(bg="purple", fontsize=17, text=" 󰸘"),  # Icon: nf-mdi-calendar_clock
    widget.Clock(**base(bg="purple"), format="%d/%m/%Y - %H:%M "),
    widget.Systray(
        background=colors["bg0"], padding=10, icon_size=15, width=100, **powerline
    ),
    widget.TextBox(
        fmt="{}",
        # width = 30,
        foreground="ff7600",
        background=colors["bg0"],
        fontsize=14,
    ),
]

widget_defaults = dict(
    font="Sauce Code Pro Nerd Font Medium",
    fontsize=16,
    padding=3,
)

extension_defaults = widget_defaults.copy()
