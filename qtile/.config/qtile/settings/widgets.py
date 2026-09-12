from libqtile import bar
from qtile_extras import widget
from qtile_bonsai import BonsaiBar

from .theme import colors
from .widget.centered_clock import CenteredClock
from .widget.floating_count import FloatCount
from .widget.keyd_indicator import KeydIndicator

WIDGET_ICON_FONT = "HasklugNerdFont Medium"
WIDGET_TEXT_FONT = "HasklugNerdFont"


def base(fg="text", bg="bg_d"):
    return {"foreground": colors[fg], "background": colors[bg]}


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def icon_separator():
    return widget.Sep(**base(), linewidth=0, padding=0)


def icon(fg="text", bg="bg_d", fontsize=16, text="?"):
    return widget.TextBox(**base(fg, bg), fontsize=fontsize, text=text, padding=3)


def workspaces():
    return [
        BonsaiBar(
            **{
                "tab.bg_color": colors["bg_d"],
                "tab.fg_color": colors["light_grey"],
                "tab.active.bg_color": colors["bg0"],
                "tab.active.fg_color": colors["fg"],
                "container_select_mode.indicator.bg_color": colors["blue"],
                "container_select_mode.indicator.fg_color": colors["bg_d"],
                "length": bar.CALCULATED,
                "font_size": 16,
                "tab.padding": [5, 5, 5, 5],
            }
        ),
        separator(),
        current_layout(),
        separator(),
        # widget.TextBox(
        #     foreground=colors["blue"],
        #     background=colors["bg_d"],
        #     font=WIDGET_ICON_FONT,
        #     text="  ",
        # ),
        # widget.Prompt(
        #     **base(fg="light_grey"),
        #     font=WIDGET_TEXT_FONT,
        #     fontsize=16,
        #     cursor=False,
        #     fmt="{}",
        #     prompt="",
        # ),
        # separator(),
    ]


def checkupdate(command="checkupdates"):
    return widget.CheckUpdates(
        background=colors["bg_d"],
        colour_have_updates=colors["cyan"],
        colour_no_updates=colors["cyan"],
        display_format=" 󰮯 {updates} ",
        no_update_string=" 󰮯 0 ",
        foreground=colors["cyan"],
        font=WIDGET_ICON_FONT,
        update_interval=1800,
        custom_command=command,
    )


def battery(bat):
    return widget.Battery(
        background=colors["bg_d"],
        battery=bat,
        discharge_char="󰁿",
        not_charging_char="󱧥",
        charge_char="",
        full_char="󰁹",
        empty_char="󱟩",
        format="{char} {percent:2.0%} ",
        foreground=colors["green"],
        font=WIDGET_ICON_FONT,
        show_short_text=False,
        low_percentage=0.05,
        low_foreground=colors["red"],
        notify_below=5,
        update_interval=60,
    )


def disk_free():
    return widget.DF(
        background=colors["bg_d"],
        partition="/home",
        format="{uf:.0f}{m}",
        fmt=" 󰋊 {}  ",
        foreground=colors["red"],
        font=WIDGET_ICON_FONT,
        visible_on_warn=False,
        update_interval=600,
    )


def net():
    return widget.Net(
        **base(bg="bg_d", fg="light_grey"),
        interface="wlan0",
        format="  {down:03.0f}{down_suffix:<2}  {up:03.0f}{up_suffix:<2} ",
        foreground=colors["blue"],
        font=WIDGET_ICON_FONT,
        prefix="k",
        update_interval=60,
    )


def wlan():
    return widget.Wlan(
        background=colors["bg_d"],
        format=" 󰢾 {percent:2.0%} ",
        disconnected_message=" 󰢿 offline ",
        foreground=colors["purple"],
        font=WIDGET_ICON_FONT,
        update_interval=60,
    )


def _bluetooth_poll():
    import subprocess

    try:
        out = subprocess.check_output(
            ["bluetoothctl", "devices", "Connected"], text=True, timeout=2
        )
        for line in out.splitlines():
            if line.startswith("Device "):
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    name = parts[2]
                    try:
                        info = subprocess.check_output(
                            ["bluetoothctl", "info", parts[1]], text=True, timeout=2
                        )
                        for l in info.splitlines():
                            if "Battery Percentage" in l:
                                pct = l.split("(")[-1].split(")")[0]
                                if pct:
                                    return f"{name} ({pct})"
                    except Exception:
                        pass
                    return name
        return "inactive"
    except Exception:
        return "inactive"


def bluetooth():
    try:
        from qtile_extras.widget.bluetooth import Bluetooth as _Bt

        class _BluetoothInactive(_Bt):
            def refresh(self):
                super().refresh()
                if not self._lines or not self._lines[0][0]:
                    txt = self.default_text
                    if "{connected_devices}" in txt:
                        txt = txt.format(
                            connected_devices="inactive",
                            num_connected_devices=0,
                            adapters="",
                            num_adapters=len(self.adapters),
                        )
                    else:
                        txt = "inactive"
                    self._lines = [(txt, lambda: None)]
                    self.show_line()

        return _BluetoothInactive(
            background=colors["bg_d"],
            foreground=colors["light_grey"],
            font="HasklugNerdFont",
            default_text="{connected_devices}",
            default_show_battery=True,
            device_battery_format=" ({battery}%)",
            device_format="{name}{battery_level} [{symbol}]",
            fmt="{} ",
        )
    except Exception:
        return widget.GenPollText(
            background=colors["bg_d"],
            foreground=colors["light_grey"],
            font="HasklugNerdFont",
            fmt="{} ",
            func=_bluetooth_poll,
            update_interval=10,
        )


def current_layout():
    return widget.CurrentLayout(
        background=colors["bg_d"],
        foreground=colors["light_grey"],
        font="HasklugNerdFont",
        fmt=" {} ",
        padding=5,
    )


def _dnd_poll():
    try:
        from subprocess import check_output

        status = check_output(["dunstctl", "is-paused"], timeout=2).strip()
        return status == b"true"
    except Exception:
        return False


def dnd():
    return widget.DoNotDisturb(
        background=colors["bg_d"],
        foreground=colors["fg"],
        font=WIDGET_ICON_FONT,
        padding=0,
        enabled_icon="󰂛 ",
        disabled_icon="󰂚 ",
        poll_function=_dnd_poll,
        update_interval=1,
    )


def window_count():
    return widget.WindowCount(
        background=colors["bg_d"],
        foreground=colors["blue"],
        font=WIDGET_ICON_FONT,
        text_format=" 󰖯 {num} ",
        show_zero=True,
    )


widgets = [
    *workspaces(),
    icon_separator(),
    checkupdate(),
    icon_separator(),
    disk_free(),
    icon_separator(),
    battery(0),
    icon_separator(),
    battery(1),
    icon_separator(),
    FloatCount(
        background=colors["bg_d"],
        format=" 󰖲 {count} ",
        foreground=colors["yellow"],
        font=WIDGET_ICON_FONT,
    ),
    icon_separator(),
    window_count(),
    icon_separator(),
    wlan(),
    icon_separator(),
    widget.Spacer(length=bar.STRETCH, background=colors["bg_d"]),
    CenteredClock(
        background=colors["bg_d"],
        format="%H:%M",
        fmt=" 󰞌 {} ",
        foreground=colors["orange"],
        font=WIDGET_ICON_FONT,
        name="clock_time",
    ),
    widget.Spacer(length=bar.STRETCH, background=colors["bg_d"]),
    separator(),
    widget.WidgetBox(
        name="windowname_box",
        widgets=[
            widget.WindowName(
                **base(fg="light_grey"),
                font=WIDGET_TEXT_FONT,
                fontsize=16,
                padding=3,
                format="{name} - {class}  ",
                max_chars=60,
                stretch=False,
            )
        ],
        text_closed=" 󰘖 ",
        text_open=" 󰘕 ",
        fontsize=16,
        font=WIDGET_TEXT_FONT,
        foreground=colors["light_grey"],
        background=colors["bg_d"],
        close_button_location="left",
    ),
    separator(),
    bluetooth(),
    separator(),
    widget.Clock(
        **base(bg="bg_d", fg="light_grey"),
        format="%a %d %b",
        fmt=f'<span font="HasklugNerdFont Bold" foreground="{
            colors["cyan"][0]
        }"> 󰃭 </span><span font="HasklugNerdFont" foreground="{
            colors["light_grey"][0]
        }">{{}} </span>',
        name="clock_date",
    ),
    separator(),
    widget.TextBox(**base(bg="bg_d", fg="fg"), text=""),  # text_box 2
    widget.TextBox(
        foreground=colors["fg"],
        background=colors["bg_d"],
        font=WIDGET_ICON_FONT,
        text=" 󰧺 ",
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
    separator(),
    dnd(),
    KeydIndicator(
        foreground=colors["light_grey"],
        background=colors["bg_d"],
        font=WIDGET_ICON_FONT,
        name="keyd",
    ),  # vim-mode indicator
    separator(),
    separator(),
]

widget_defaults = dict(
    font="HasklugNerdFont",
    fontsize=16,
    padding=3,
    foreground=colors["light_grey"],
    background=colors["bg_d"],
)

extension_defaults = widget_defaults.copy()
extension_defaults = widget_defaults.copy()
