from libqtile import bar
from qtile_extras import widget
from qtile_bonsai import BonsaiBar

from .theme import colors
from .widget.centered_clock import CenteredClock
from .widget.floating_count import FloatCount
from .widget.keyd_indicator import KeydIndicator


def base(fg="text", bg="bg_d"):
    return {"foreground": colors[fg], "background": colors[bg]}


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def icon(fg="text", bg="bg_d", fontsize=16, text="?"):
    return widget.TextBox(**base(fg, bg), fontsize=fontsize, text=text, padding=3)


def workspaces():
    return [
        BonsaiBar(
            **{
                "tab.bg_color": "#21252b",
                "tab.fg_color": "#9da5b4",
                "tab.active.bg_color": "#21252b",
                "tab.active.fg_color": "#dcdcdc",
                "container_select_mode.indicator.bg_color": colors["blue"],
                "container_select_mode.indicator.fg_color": "#21252b",
                "length": bar.CALCULATED,
                "font_size": 16,
                "tab.padding": [15, 5, 15, 5],
            }
        ),
        separator(),
        widget.TextBox(
            **base(fg="light_grey"),
            fmt=f'<span font="HasklugNerdFont Bold" foreground="{
                colors["blue"][0]
            }">  </span>',
        ),
        widget.Prompt(
            **base(fg="light_grey"),
            font="HasklugNerdFont",
            fontsize=13,
            cursor=False,
            fmt="{}",
            prompt="",
        ),
        separator(),
        widget.WidgetBox(
            name="windowname_box",
            widgets=[
                widget.WindowName(
                    **base(fg="light_grey"),
                    font="HasklugNerdFont",
                    fontsize=13,
                    padding=5,
                    format="{name} - {class}",
                )
            ],
            text_closed=" 󰘖 ",
            text_open=" 󰘕 ",
            fontsize=13,
            font="HasklugNerdFont",
            foreground=colors["light_grey"],
            background=colors["bg_d"],
            close_button_location="left",
        ),
        separator(),
    ]


def checkupdate(command="checkupdates"):
    return widget.CheckUpdates(
        background=colors["bg_d"],
        colour_have_updates=colors["light_grey"],
        colour_no_updates=colors["light_grey"],
        display_format=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["yellow"][0]
        }"> 󰮯 </span>'
        + "{updates} ",
        no_update_string=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["yellow"][0]
        }"> 󰮯 </span>'
        + "0 ",
        update_interval=1800,
        custom_command=command,
    )


def battery(bat):
    return widget.Battery(
        **base(fg="light_grey"),
        battery=bat,
        discharge_char="󰁿",
        not_charging_char="󱧥",
        charge_char="",
        full_char="󰁹",
        empty_char="󱟩",
        format=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["green"][0]
        }">{{char}}</span> {{percent:2.0%}} ',
        show_short_text=False,
        low_percentage=0.05,
        low_foreground=colors["red"],
        notify_below=5,
        update_interval=60,
    )


def disk_free():
    return widget.DF(
        **base(fg="light_grey"),
        partition="/home",
        format="{uf:.0f}{m}",
        fmt=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["red"][0]
        }">󰋊 </span>'
        + "{}  ",
        visible_on_warn=False,
        update_interval=600,
    )


def net():
    return widget.Net(
        **base(bg="bg_d", fg="light_grey"),
        interface="wlan0",
        format=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["blue"][0]
        }">  </span>'
        + "{down:03.0f}{down_suffix:<2}"
        + f'<span font="HasklugNerdFont Bold" foreground="{
            colors["blue"][0]
        }">  </span>'
        + "{up:03.0f}{up_suffix:<2} ",
        prefix="k",
        update_interval=60,
    )


def wlan():
    return widget.Wlan(
        **base(bg="bg_d", fg="light_grey"),
        format=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["purple"][0]
        }"> 󰢾 </span>'
        + "{percent:2.0%} ",
        disconnected_message=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["red"][0]
        }"> 󰢿 </span>'
        + "offline ",
        update_interval=60,
    )


def bluetooth():
    return widget.Bluetooth(
        **base(bg="bg_d", fg="light_grey"),
        default_text="{connected_devices}",
        device_format="Device: {battery_level}[{symbol}]",
        fmt=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["cyan"][0]
        }"> 󰥰 </span>'
        + "{} ",
    )


widgets = [
    *workspaces(),
    widget.Spacer(length=bar.STRETCH, background=colors["bg_d"]),
    CenteredClock(
        **base(bg="bg_d", fg="light_grey"),
        format="%H:%M",
        fmt=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["orange"][0]
        }"> 󰞌 </span>'
        + "{} ",
        name="clock_time",
    ),
    widget.Spacer(length=bar.STRETCH, background=colors["bg_d"]),
    widget.Sep(**base(bg="bg_d", fg="bg_d"), linewidth=16),
    disk_free(),
    battery(0),
    battery(1),
    checkupdate(),
    FloatCount(
        **base(bg="bg_d", fg="light_grey"),
        format=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["blue"][0]
        }"> 󰖲 </span>'
        + "{count} ",
    ),
    # net(),
    wlan(),
    widget.Clock(
        **base(bg="bg_d", fg="light_grey"),
        format="%a %d %b",
        fmt=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["cyan"][0]
        }"> 󰃭 </span>'
        + "{} ",
        name="clock_date",
    ),
    widget.TextBox(
        **base(bg="bg_d", fg="light_grey"),
        text=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["light_grey"][0]
        }">󰧺 </span>',
    ),  # text_box 1
    # text_box 2 — mic status (noise-supression)
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 3
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 4
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 5
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 6
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 7
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 8
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 9
    KeydIndicator(
        **base(bg="bg_d", fg="light_grey"), font="HasklugNerdFont Bold", name="keyd"
    ),  # vim-mode indicator
    widget.Sep(background=colors["bg_d"], foreground=colors["bg_d"], linewidth=10),
]

widget_defaults = dict(
    font="HasklugNerdFont",
    fontsize=16,
    padding=3,
    foreground=colors["light_grey"],
    background=colors["bg_d"],
)

extension_defaults = widget_defaults.copy()
