#  _________________________________________________________
#    ___   _    _  _                             __  _  __ _
#   / _ \ | |_ (_)| | ___        __  ___  _ _   / _|(_)/ _` |
#  | (_) ||  _|| || |/ -_)      / _|/ _ \| ' \ |  _|| |\__. |
#   \__\_\ \__||_||_|\___|      \__|\___/|_||_||_|  |_||___/
#  _________________________________________________________




from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

from libqtile import bar, layout, qtile
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), lazy.layout.shrink(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), lazy.layout.grow(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

	# Keybind for apps
    #Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    KeyChord([mod], "Return", [
        Key([], "t", lazy.spawn("alacritty -e tmux")),
        Key([], "a", lazy.spawn("alacritty -e tmux a")),
        Key([], "Return", lazy.spawn("alacritty")),
        ]),
	Key([mod], "Escape", lazy.spawn("dunstctl close-all")),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),
	Key([mod, "shift"], "b", lazy.spawn("qutebrowser -T")),
	Key([mod], "a", lazy.spawn("rofi -show drun")),
    Key([mod], "d", lazy.spawn("drawing")),
	Key([mod], "b", lazy.spawn("qutebrowser")),
	Key([mod], "o", lazy.spawn("okular")),

	# Keybinds for Script
    #Key([mod], "F2", lazy.spawn("./.myscript/touchpad_tg.sh")),
	Key([mod], "F1", lazy.spawn("pamixer -t")), 
	Key([mod], "F2", lazy.spawn("pamixer -d 5")), 
    Key([mod], "F3", lazy.spawn("pamixer -i 5")),
	Key([mod], "F5", lazy.spawn("brightnessctl set 5%-")),
	Key([mod], "F6", lazy.spawn("brightnessctl set +5%")),
	Key([mod], "F7", lazy.spawn("sh /usr/local/bin/uptime-notification")),
	Key([mod], "F11", lazy.spawn("vktablet")),
	Key([mod], "End", lazy.spawn("sh /usr/local/bin/lock-screen")),
	Key([mod], "Space", lazy.spawn("sh /usr/local/bin/toggle-trackpoint")),

	# Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod, "shift"], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7"]
#group_labels = ["", "☎","☰", "", "", "", "",]
group_labels = ["NETS ❯", "COMS ❯","NOTE ❯", "FILE ❯", "CODE ❯", "IMAG ❯", "VIDS ❯",]
group_layouts = ["MonadTall", "MonadTall", "MonadThreeCol", "MonadThreeCol", "MonadTall", "MonadTall", "MonadThreeCol",]


for i in range(len(group_names)):
	groups.append(
		Group(
			name=group_names[i],
			layout=group_layouts[i].lower(),
			label=group_labels[i],
        ))

for i in groups:
	keys.extend([
		Key([mod], i.name, lazy.group[i.name].toscreen()),
        #Key([mod], "Tab", lazy.screen.next_group()),
        #Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
        Key([mod, "control"], i.name, lazy.window.togroup(i.name)),
    ])

groups.append(ScratchPad("scratchpad", [
    DropDown("music", "alacritty --class=music -e ytfzf --type=all --pages=5 -sml", width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9),
    DropDown("cpustats", "alacritty --class=monitor -e auto-cpufreq --stats", width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9),
    DropDown("nmfzf", "alacritty --class=nmcli-fzf -e bash .myscript/nm-wifi.fzf.sh", on_focus_lost_hide = False, width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9),
    DropDown("calculator", "alacritty --class=calc -e python -i /usr/local/bin/calc", width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9),
    DropDown("youtube", "alacritty --class=music -e ytfzf --type=all --detach --pages=5 -sl", width=0.7, height=0.8, x=0.15, y =0.1, opacity=0.9),
    DropDown("tyoutube", "alacritty --class=music -e ytfzf --type=all --detach --pages=5 -stl", width=0.7, height=0.8, x=0.15, y =0.1, opacity=0.9),
    DropDown("shellgpt", "alacritty --class=shellgpt -e bash --rcfile ~/.config/shell_gpt/bashrc", width=0.6, height=0.6, x=0.2, y =0.2, opacity=0.9),
    DropDown("ranger", "alacritty --class=ranger -e ranger", width=0.6, height=0.6, x=0.2, y =0.2, opacity=0.9),
    DropDown("bottom", "alacritty --class=monitor -e btm", width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("typing", "alacritty --class=racer -o font.size=11.5 -e tt -theme mine", width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("okular", "okular", on_focus_lost_hide= False, width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("drawing", "rnote", on_focus_lost_hide= False, width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("mpv", "mpv /tmp/open &", width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("terminal", terminal, width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
    DropDown("discord", "discord", width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9),
]))

keys.extend([
    KeyChord([mod], "y", [
        Key([], "y", lazy.group['scratchpad'].dropdown_toggle('youtube') ,desc="Launch ytfzf"),
        Key([], "m", lazy.group['scratchpad'].dropdown_toggle('music') ,desc="Launch ytfzf"),
        Key([], "t", lazy.group['scratchpad'].dropdown_toggle('tyoutube') ,desc="Launch ytfzf"),
        ]),
    Key([mod], "g", lazy.group['scratchpad'].dropdown_toggle('shellgpt')),
    KeyChord([mod], "m", [
        Key([], "f", lazy.group['scratchpad'].dropdown_toggle('ranger') ,desc="Launch ranger"),
        Key([], "s", lazy.group['scratchpad'].dropdown_toggle('bottom') ,desc="Launch bottom"),
        Key([], "c", lazy.group['scratchpad'].dropdown_toggle('cpustats') ,desc="Launch bottom"),
        ]),
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('nmfzf')),
    Key([mod], "c", lazy.group['scratchpad'].dropdown_toggle('calculator')),
    Key([mod], "t", lazy.group['scratchpad'].dropdown_toggle('typing')),
    Key([mod], "d", lazy.group['scratchpad'].dropdown_toggle('discord')),
    Key([mod, "control"], "o", lazy.group['scratchpad'].dropdown_toggle('okular')),
    Key([mod, "control"], "d", lazy.group['scratchpad'].dropdown_toggle('drawing')),
    Key([mod, "control"], "p", lazy.group['scratchpad'].dropdown_toggle('mpv')),
    Key([mod, "control"], "Return", lazy.group['scratchpad'].dropdown_toggle('terminal')),
])

layout_theme = {
	"border_width" : 0,
	"margin" : 15,
	"border_focus" : "FFFFFF",
	"border_normal" : "CCCCCC"
}

layouts = [
    layout.MonadTall(**layout_theme),
	layout.MonadThreeCol(
		**layout_theme,
		main_centered=True,
		new_client_position = 'bottom',
		ratio = 0.34
	),
]

widget_defaults = dict(
    font="sans",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

powerline = {
    "decorations": [
        PowerLineDecoration(path="arrow_right")
    ]
}

screens = [
    Screen(
        top=bar.Bar(
            [
				widget.Spacer(
					length = 0,
				),

                widget.GroupBox(
					foreground ='000000',
					center_aligned = True,
					border = 'ff00ff',
                    inactive = '232323',
					active = '404040',
                    highlight_method = "text",
                    font = 'sans bold',
					rounded = True,
					this_current_screen_border = 'FF00FF',
					pading = 10,
				),

				widget.Sep(
					foreground = "a20640",
					linewidth = 0,
					size_percent = 60,
					padding = 13,
				),

				widget.TextBox(
					fmt = "[]= {}",
					width = 30,
                    foreground = '00ffff',
					fontsize = 14,
				),

                widget.Prompt(
			    	fmt = "{}",
                    foreground="00FFFF",
			    	prompt = "",
			    	scroll_fixed_width = True,
			    ),

				widget.Spacer(
					width = 950,
				),
                
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                widget.Systray(
					background = '000000',
					icon_size = 15,
					padding = 10,
					width = 50,
                    **powerline
				),

				widget.Spacer(
                    length=1,
                    **powerline
                ),

                widget.Battery(
                    foreground = '000000',
                    background = '00FF00',
                    low_foreground = '000000',
                    battery = 1,
                    discharge_char = '',
                    not_charging_char = '',
                    charge_char = '',
                    full_char = '',
                    empty_char = '󱉝',
                    show_short_text = False,
                    format = '1: {char}  {percent:2.0%}',
                    low_percent = 0.4,
                    notify_below = 0.45,
                    update_interval = 60,
                    **powerline
                ),

                widget.Battery(
                    foreground = '000000',
                    background = '00FF00',
                    low_foreground = '000000',
                    battery = 0,
                    discharge_char = '',
                    not_charging_char = '',
                    charge_char = '',
                    full_char = '',
                    empty_char = '󱉝',
                    show_short_text = False,
                    format = '❮   0: {char}  {percent:2.0%}',
                    low_percent = 0.4,
                    notify_below = 0.45,
                    update_interval = 60,
                    padding = 10,
                    **powerline
                ),

                widget.CheckUpdates(
                    foreground = 'ffffff',
                    background = 'AE00FF',
                    colour_have_updates = '000000',
                    colour_no_updates = '000000',
                    distro='Arch',
				  	fmt = "  {}",
                    padding = 10,
                    no_update_string ="Up to date",
                    update_interval = 360,
                    **powerline
                ),
                 # widget.CurrentLayout(
				 # 	foreground = '000000',
				 # 	background = 'C30046',
				 # 	fmt = " {}",
				 # 	padding = 10,
				 # 	scroll_fixed_width = True,
                 #     **powerline
				 # ),

				widget.Volume(
					foreground = '000000',
					background = '00FFFF',
					fmt = "♪   {}",
                    get_volume_command = 'echo $(pamixer --get-volume)%',
                    check_mute_command = 'pamixer --get-mute',
                    check_mute_string = 'true',
					padding = 10,
					scroll_fixed_width = True,
                    **powerline
				),

                widget.Wlan(
                    background = '00FFFF',
                    foreground = '000000',
                    format = '❮       {percent:1.0%}  ',
                    width = 115,
                    update_internal = 60,
                ),

                widget.Backlight(
					background = '00FFFF',
                    foreground = '000000',
                    format = '❮  ☀   {percent:2.0%}  ',
                    backlight_name = 'intel_backlight',
                    **powerline
                ),

				widget.Clock(
                    background = 'FF005C',
					foreground = '000000',
					fmt = "   {}",
					format="%I:%M %p",
					padding = 10,
                    **powerline
				),

                #widget.QuickExit(
				#	foreground = '000000',
				#	background = 'FF00FF',
				#	default_text = '[X]',
				#	countdown_format = '[{}]',
				#	padding = 0,
                #    **powerline
				#),

				widget.Spacer(
                    background = 'FF005C',
					length = -1, 
				),
            ],
            26,
            margin = [5, 15, 0, 15],
            #border_width=[4, 0, 4, 0],  # Draw top and bottom borders
            #border_color=["000000", "000000", "000000", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimjize = True
wl_input_rules = None
wmname = "LG3D"
