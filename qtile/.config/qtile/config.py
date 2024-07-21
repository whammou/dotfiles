from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

from qtile_bonsai import Bonsai, BonsaiBar

from libqtile import bar, layout, qtile
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key,EzKey, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [

	Key([mod], "Escape", lazy.spawn("dunstctl close-all")),

    # Open your terminal emulator quickly. See further below for how to
    # directly open other apps as splits/tabs using something like rofi.

    KeyChord(
        ["mod4"],
        "y",
        [
            KeyChord([], "q",
                [
                   EzKey("b", lazy.layout.spawn_split("qb", 'y', position='next')),
                   EzKey("d", lazy.layout.spawn_split("discord", 'y', position='next')),
                   EzKey("t", lazy.layout.spawn_split("teams", 'y', position='next')),
                ]
            ),
            KeyChord([], "t",
                [
                    EzKey("1", lazy.layout.spawn_split("tmux-session-attach 1", 'y', position='next')),
                    EzKey("2", lazy.layout.spawn_split("tmux-session-attach 2", 'y', position='next')),
                    EzKey("3", lazy.layout.spawn_split("tmux-session-attach 3", 'y', position='next')),
                    EzKey("4", lazy.layout.spawn_split("tmux-session-attach 4", 'y', position='next')),
                ]
            ),
            KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_split("ssh-tmux 1", "y", position="next")),
                    EzKey("2", lazy.layout.spawn_split("ssh-tmux 2", "y", position="next")),
                    EzKey("3", lazy.layout.spawn_split("ssh-tmux 3", "y", position="next")),
                    EzKey("4", lazy.layout.spawn_split("ssh-tmux 4", "y", position="next")),
                ]
            ),

        ]
    ),
    
    KeyChord(
        ["mod4"],
        "x",
        [
            KeyChord([],"q",
                [
                    EzKey("b", lazy.layout.spawn_split("qb", 'x', position='next')),
                    EzKey("d", lazy.layout.spawn_split("discord", 'x', position='next')),
                    EzKey("t", lazy.layout.spawn_split("teams", 'x', position='next')),
                ]
            ),
            KeyChord([], "t",
                [
                   EzKey("1", lazy.layout.spawn_split("tmux-session-attach 1", 'x', position='next')),
                   EzKey("2", lazy.layout.spawn_split("tmux-session-attach 2", 'x', position='next')),
                   EzKey("3", lazy.layout.spawn_split("tmux-session-attach 3", 'x', position='next')),
                   EzKey("4", lazy.layout.spawn_split("tmux-session-attach 4", 'x', position='next')),
                ]
            ),
            KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_split("ssh-tmux 1", "x", position="next")),
                    EzKey("2", lazy.layout.spawn_split("ssh-tmux 2", "x", position="next")),
                    EzKey("3", lazy.layout.spawn_split("ssh-tmux 3", "x", position="next")),
                    EzKey("4", lazy.layout.spawn_split("ssh-tmux 4", "x", position="next")),
                ]
            ),
        ]
    ),

    KeyChord(
        ["mod4"],
        "t",
        [
            KeyChord([],"q",
                [
                    EzKey("b", lazy.layout.spawn_tab("qb")),
                ]
            ),
            KeyChord([], "t",
                [
                    EzKey("1", lazy.layout.spawn_tab("tmux-session-attach 1")),
                    EzKey("2", lazy.layout.spawn_tab("tmux-session-attach 2")),
                    EzKey("3", lazy.layout.spawn_tab("tmux-session-attach 3")),
                    EzKey("4", lazy.layout.spawn_tab("tmux-session-attach 4")),
                ]
            ),
            KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_tab("ssh-tmux 1")),
                    EzKey("2", lazy.layout.spawn_tab("ssh-tmux 2")),
                    EzKey("3", lazy.layout.spawn_tab("ssh-tmux 3")),
                    EzKey("4", lazy.layout.spawn_tab("ssh-tmux 4")),
                ]
            ),
        ]

    ),
    KeyChord(
        ["mod4", "Shift"],
        "t",
        [
            KeyChord([],"q",
                [
                    EzKey("b", lazy.layout.spawn_tab("qb", new_level=True)),
                ]
            ),
            KeyChord([], "t",
                [
                    EzKey("1", lazy.layout.spawn_tab("tmux-session-attach 1", new_level=True)),
                    EzKey("2", lazy.layout.spawn_tab("tmux-session-attach 2", new_level=True)),
                    EzKey("3", lazy.layout.spawn_tab("tmux-session-attach 3", new_level=True)),
                    EzKey("4", lazy.layout.spawn_tab("tmux-session-attach 4", new_level=True)),
                ]
            ),
            KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_tab("ssh-tmux 1", new_level=True)),
                    EzKey("2", lazy.layout.spawn_tab("ssh-tmux 2", new_level=True)),
                    EzKey("3", lazy.layout.spawn_tab("ssh-tmux 3", new_level=True)),
                    EzKey("4", lazy.layout.spawn_tab("ssh-tmux 4", new_level=True)),
                ]
            ),
        ]
    ),
    
    # Sometimes it's handy to have a split open in the 'previous' position
    KeyChord(
        ["mod4", "Shift"],
        "y",
        [
            KeyChord([], "q",
                [
                   EzKey("b", lazy.layout.spawn_split("qb", 'y', position='previous')),
                ]
            ),
            KeyChord([], "t",
                [
                    EzKey("1", lazy.layout.spawn_split("tmux-session-attach 1", 'y', position='previous')),
                    EzKey("2", lazy.layout.spawn_split("tmux-session-attach 2", 'y', position='previous')),
                    EzKey("3", lazy.layout.spawn_split("tmux-session-attach 3", 'y', position='previous')),
                    EzKey("4", lazy.layout.spawn_split("tmux-session-attach 4", 'y', position='previous')),
                ]
            ),
            KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_split("ssh-tmux 1", "y", position="next")),
                    EzKey("2", lazy.layout.spawn_split("ssh-tmux 2", "y", position="next")),
                    EzKey("3", lazy.layout.spawn_split("ssh-tmux 3", "y", position="next")),
                    EzKey("4", lazy.layout.spawn_split("ssh-tmux 4", "y", position="next")),
                ]
            ),
        ]
    ),
    
    KeyChord(
        ["mod4", "Shift"],
        "x",
        [
            KeyChord([],"q",
                [
                    EzKey("b", lazy.layout.spawn_split("qb", 'x', position='previous')),
                ]
            ),
            KeyChord([], "t",
                [
                    EzKey("1", lazy.layout.spawn_split("tmux-session-attach 1", 'x', position='previous')),
                    EzKey("2", lazy.layout.spawn_split("tmux-session-attach 2", 'x', position='previous')),
                    EzKey("3", lazy.layout.spawn_split("tmux-session-attach 3", 'x', position='previous')),
                    EzKey("4", lazy.layout.spawn_split("tmux-session-attach 4", 'x', position='previous')),
                ]
            ), KeyChord(["Shift"], "t", 
                [
                    EzKey("1", lazy.layout.spawn_split("ssh-tmux 1", "x", position="next")),
                    EzKey("2", lazy.layout.spawn_split("ssh-tmux 2", "x", position="next")),
                    EzKey("3", lazy.layout.spawn_split("ssh-tmux 3", "x", position="next")),
                    EzKey("4", lazy.layout.spawn_split("ssh-tmux 4", "x", position="next")),
                ]
            ),
        ]
    ),

    # Motions to move focus. The names are compatible with built-in layouts.
    EzKey("M-h", lazy.layout.move_focus("left", wrap=False)),
    EzKey("M-l", lazy.layout.move_focus("right", wrap=False)),
    EzKey("M-k", lazy.layout.move_focus("up", wrap=False)),
    EzKey("M-j", lazy.layout.move_focus("down", wrap=False)),


    # Precise motions to move directly to specific tabs at the nearest tab level
    EzKey("M-1", lazy.layout.focus_nth_tab(1, level=-1)),
    EzKey("M-2", lazy.layout.focus_nth_tab(2, level=-1)),
    EzKey("M-3", lazy.layout.focus_nth_tab(3, level=-1)),
    EzKey("M-4", lazy.layout.focus_nth_tab(4, level=-1)),
    EzKey("M-5", lazy.layout.focus_nth_tab(5, level=-1)),
    
    # Precise motions to move directly to specific tabs at the nearest tab level
    EzKey("M-S-1", lazy.layout.focus_nth_tab(1, level=1)),
    EzKey("M-S-2", lazy.layout.focus_nth_tab(2, level=1)),
    EzKey("M-S-3", lazy.layout.focus_nth_tab(3, level=1)),
    EzKey("M-S-4", lazy.layout.focus_nth_tab(4, level=1)),
    EzKey("M-S-5", lazy.layout.focus_nth_tab(5, level=1)),

    # Precise motions to move to specific windows. The options provided here let
    # us pick the nth window counting only from under currently active [sub]tabs
    EzKey("A-1", lazy.layout.focus_nth_window(1, ignore_inactive_tabs_at_levels=[1,2])),
    EzKey("A-2", lazy.layout.focus_nth_window(2, ignore_inactive_tabs_at_levels=[1,2])),
    EzKey("A-3", lazy.layout.focus_nth_window(3, ignore_inactive_tabs_at_levels=[1,2])),
    EzKey("A-4", lazy.layout.focus_nth_window(4, ignore_inactive_tabs_at_levels=[1,2])),
    EzKey("A-5", lazy.layout.focus_nth_window(5, ignore_inactive_tabs_at_levels=[1,2])),

    # Resize operations
    EzKey("M-C-h", lazy.layout.resize("left", 100)),
    EzKey("M-C-l", lazy.layout.resize("right", 100)),
    EzKey("M-C-k", lazy.layout.resize("up", 100)),
    EzKey("M-C-j", lazy.layout.resize("down", 100)),

    # Swap windows/tabs with neighbors
    EzKey("M-S-h", lazy.layout.swap("left")),
    EzKey("M-S-l", lazy.layout.swap("right")),
    EzKey("M-S-k", lazy.layout.swap("up")),
    EzKey("M-S-j", lazy.layout.swap("down")),
    EzKey("A-S-d", lazy.layout.swap_tabs("previous")),
    EzKey("A-S-f", lazy.layout.swap_tabs("next")),
    
    # Manipulate selections after entering container-select mode
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),

    # It's kinda nice to have more advanced window management commands under a
    # qtile key chord.
    KeyChord(
        ["mod4"],
        "w",
        [
            # Use something like rofi to pick GUI apps to open as splits/tabs.
            #EzKey("v", lazy.layout.spawn_split(rofi_run_cmd, "x")),
            #EzKey("x", lazy.layout.spawn_split(rofi_run_cmd, "y")),
            #EzKey("t", lazy.layout.spawn_tab(rofi_run_cmd)),
            #EzKey("S-t", lazy.layout.spawn_tab(rofi_run_cmd, new_level=True)),
            
            # Toggle container-selection mode to split/tab over containers of
            # multiple windows. Manipulate using select_container_outer()/select_container_inner()
            EzKey("C-v", lazy.layout.toggle_container_select_mode()),
            EzKey("o", lazy.layout.pull_out()),
            EzKey("u", lazy.layout.pull_out_to_tab()),
            EzKey("r", lazy.layout.rename_tab()),
            
            # Directional commands to merge windows with their neighbor into subtabs.
            KeyChord(
                [],
                "m",
                [
                    EzKey("h", lazy.layout.merge_to_subtab("left")),
                    EzKey("l", lazy.layout.merge_to_subtab("right")),
                    EzKey("j", lazy.layout.merge_to_subtab("down")),
                    EzKey("k", lazy.layout.merge_to_subtab("up")),

                    # Merge entire tabs with each other as splits
                    EzKey("S-h", lazy.layout.merge_tabs("previous")),
                    EzKey("S-l", lazy.layout.merge_tabs("next")),
                ],
            ),
            
            # Directional commands for push_in() to move window inside neighbor space.
            KeyChord(
                [],
                "i",
                [
                    EzKey("j", lazy.layout.push_in("down")),
                    EzKey("k", lazy.layout.push_in("up")),
                    EzKey("h", lazy.layout.push_in("left")),
                    EzKey("l", lazy.layout.push_in("right")),
                    
                    # It's nice to be able to push directly into the deepest
                    # neighbor node when desired. The default bindings above
                    # will have us push into the largest neighbor container.
                    EzKey(
                        "S-j",
                        lazy.layout.push_in("down", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "S-k",
                        lazy.layout.push_in("up", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "S-h",
                        lazy.layout.push_in("left", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "S-l",
                        lazy.layout.push_in("right", dest_selection="mru_deepest"),
                    ),
                ],
            ),
        ]
    ),
    
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    ## Toggle between split and unsplit sides of stack.
    ## Split = all windows displayed
    ## Unsplit = 1 window displayed, like Max layout, but still with
    ## multiple stack panes
    #Key(
    #    [mod, "shift"],
    #    "Return",
    #    lazy.layout.toggle_split(),
    #    desc="Toggle between split and unsplit sides of stack",
    #),
    #Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    ## Toggle between different layouts as defined below
    #Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod], "p", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

	# Keybinds for Script
    #Key([mod], "F2", lazy.spawn("./.myscript/touchpad_tg.sh")),
	Key([mod], "F1", lazy.spawn("pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle")), 
	Key([mod], "F2", lazy.spawn("dec-volume-notification")), 
    Key([mod], "F3", lazy.spawn("inc-volume-notification")),
    Key([mod], "F4", lazy.spawn("pactl set-source-mute 0 toggle")),
    Key([mod, "Shift"], "F4", lazy.spawn("noise-supression")),
	Key([mod], "F5", lazy.spawn("brightnessctl set 5%-")),
	Key([mod], "F6", lazy.spawn("brightnessctl set +5%")),
	Key([mod], "F7", lazy.spawn("uptime-notification")),
	Key([mod], "F11", lazy.spawn("vktablet")),
	Key([mod], "Space", lazy.spawn("sh /usr/local/bin/toggle-trackpoint")),

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
#for vt in range(1, 8):
#    keys.append(
#        Key(
#            ["control", "mod1"],
#            f"f{vt}",
#            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#            desc=f"Switch to VT{vt}",
#        )
#    )


groups = [Group(i) for i in "123456789"]
#
#for i in groups:
#    keys.extend(
#        [
#            # mod + group number = switch to group
#            Key(
#                [mod],
#                i.name,
#                lazy.group[i.name].toscreen(),
#                desc="Switch to group {}".format(i.name),
#            ),
#            # mod + shift + group number = switch to & move focused window to group
#            Key(
#                [mod, "shift"],
#                i.name,
#                lazy.window.togroup(i.name, switch_group=True),
#                desc="Switch to & move focused window to group {}".format(i.name),
#            ),
#            # Or, use below if you prefer not to switch to that group.
#            # # mod + shift + group number = move focused window to group
#            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#            #     desc="move focused window to group {}".format(i.name)),
#        ]
#    )

groups.append(ScratchPad("scratchpad", [
    DropDown(
        "music", "alacritty --class=music -e ytfzf --type=all --pages=5 -sml",
        width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9
        ),
    DropDown(
        "cpustats", "alacritty --class=monitor -e sudo auto-cpufreq --monitor",
        width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9
        ),
    DropDown(
        "nmfzf", "alacritty --class=nmcli-fzf -e bash /usr/local/bin/nmwifi-fzf",
         width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9, on_focus_lost_hide = False
         ),
    DropDown(
        "calculator", "alacritty --class=calc -e python -i /usr/local/bin/calc",
        width=0.45, height=0.8, x=0.275, y =0.1, opacity=0.9
        ),
    DropDown(
        "youtube", "alacritty --class=music -e ytfzf --type=all --detach --pages=5 -sl",
        width=0.7, height=0.8, x=0.15, y =0.1, opacity=0.9
        ),
    DropDown(
        "tyoutube", "alacritty --class=music -e ytfzf --type=all --detach --pages=5 -stl",
        width=0.7, height=0.8, x=0.15, y =0.1, opacity=0.9
        ),
    DropDown(
        "shellgpt", "alacritty --class=shellgpt -e bash --rcfile ~/.config/shell_gpt/bashrc",
        width=0.6, height=0.6, x=0.2, y =0.2, opacity=0.9
        ),
    DropDown(
        "bottom", "alacritty --class=monitor -e btm",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
    DropDown(
        "typing", "alacritty --class=racer -o font.size=11.5 -e tt -theme mine",
        width=0.8, height=0.2, x=0.1, y =0.4, opacity=0.9
        ),
    DropDown(
        "drawing", "rnote",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9, on_focus_lost_hide= False
        ),
    DropDown(
        "mpv", "mpv /tmp/open &",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=1
        ),
    DropDown(
        "terminal",
        terminal, width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
    DropDown(
        "powermenu", "alacritty --class=powermenu -e power-menu",
        width=0.1, height=0.2, x=0.45, y =0.4, opacity=0.9
        ),
    DropDown(
        "qutebrowser", "qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
    DropDown(
        "discord", "qutebrowser -B /home/whammou/.config/qutebrowser/app/ https://discord.com/app",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
    DropDown(
        "teams", "qutebrowser -B /home/whammou/.config/qutebrowser/app/ 'https://teams.microsoft.com/v2/?culture=en-us&country=us'",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
    DropDown(
        "timetable", "qutebrowser -B /home/whammou/.config/qutebrowser/app/ https://mytimetable.rmit.edu.vn/even/student?ss=70b876e2e1fb477da39d8f828ddac455#timetable/grid",
        width=0.8, height=0.8, x=0.1, y =0.1, opacity=0.9
        ),
]))

keys.extend([
    Key([mod], "g", lazy.group['scratchpad'].dropdown_toggle('shellgpt')),
    Key([mod], "F8", lazy.group['scratchpad'].dropdown_toggle('nmfzf')),
    Key([mod], "Delete", lazy.group['scratchpad'].dropdown_toggle('powermenu')),
    Key([mod, "control"], "d", lazy.group['scratchpad'].dropdown_toggle('drawing')),
    Key([mod, "control"], "p", lazy.group['scratchpad'].dropdown_toggle('mpv')),
    Key([mod, "Control"], "b", lazy.group['scratchpad'].dropdown_toggle('qutebrowser')),

    KeyChord([mod], "m", [
        Key([], "p", lazy.group['scratchpad'].dropdown_toggle('bottom')),
        Key([], "c", lazy.group['scratchpad'].dropdown_toggle('cpustats')),
        ]),

    KeyChord([mod], "u", [
        Key([], "c", lazy.group['scratchpad'].dropdown_toggle('calculator')),
        Key([], "t", lazy.group['scratchpad'].dropdown_toggle('typing')),
        Key([], "y", lazy.group['scratchpad'].dropdown_toggle('youtube')),
        Key([], "m", lazy.group['scratchpad'].dropdown_toggle('music')),
        Key([], "v", lazy.group['scratchpad'].dropdown_toggle('tyoutube')),
        ]),

    KeyChord([mod, "Control"], "q", [
        Key([], "b", lazy.group['scratchpad'].dropdown_toggle('qutebrowser')),
        Key([], "d", lazy.group['scratchpad'].dropdown_toggle('discord')),
        Key([], "t", lazy.group['scratchpad'].dropdown_toggle('teams')),
        Key([], "i", lazy.group['scratchpad'].dropdown_toggle('timetable')),
        ]),
])


layouts = [
    Bonsai(**{
        "window.border_size": 0,
        "window.margin": [0, 3, 6, 3],
        "window.default.add.mode": "match_previous",
        "tab_bar.height": 6,
        "tab_bar.margin": [0, 3, 0, 3],
        "L1.tab_bar.hide_when": "always",
        "tab_bar.tab.font_size": 1,
        "tab_bar.tab.bg_color": "006767",
        "tab_bar.tab.active.bg_color": "00ffff",
        "container_select_mode.border_color": "ff00ff",
        "container_select_mode.borser_size": 1,
    }),
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
        wallpaper = '/home/whammou/.wallpaper/meteor.jpg',
        wallpaper_mode = 'fill',
        left=bar.Bar([], 6),
        right=bar.Bar(
            [],
            1,
            margin = [0, -1, 0 ,7],
        ),
        top=bar.Bar(
            [
                BonsaiBar(**{
                    "tab.bg_color": "000000",
                    "tab.fg_color": "232323",
                    "tab.active.fg_color": "00ffff",
                    "tab.active.bg_color": "000000",
                    "length": bar.CALCULATED,
                    "font_size": 18,
                    "tab.padding": [0, 10, 10 ,10],
                }),

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
                    foreground="00ffff",
			    	prompt = "",
			    	scroll_fixed_width = True,
			    ),

				widget.Spacer(
					width = 950,
				),

                widget.Chord(
                    
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
                    format = '   {char}  {percent:2.0%}  ',
                    low_percent = 0.4,
                    notify_below = 0.45,
                    update_interval = 60,
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
                    format = '❮    {char}  {percent:2.0%} ',
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
				  	fmt = "    {}  ",
                    padding = 10,
                    no_update_string ="Up to date",
                    update_interval = 360,
                    **powerline
                ),

                widget.Wlan(
                    background = '00FFFF',
                    foreground = '000000',
                    format = '     {percent:1.0%}  ',
                    update_interval = 60,
                ),

                widget.Backlight(
					background = '00FFFF',
                    foreground = '000000',
                    format = '❮    󰃞   {percent:2.0%}  ',
                    backlight_name = 'intel_backlight',
                    **powerline
                ),

				widget.Clock(
                    background = 'FF005C',
					foreground = '000000',
					fmt = "    {}  ",
					format="%I:%M %p",
					padding = 10,
                    **powerline
				),

				widget.Spacer(
                    background = 'FF005C',
					length = -1, 
				),

            ],
            26,
            margin = [6, 12 , 12, 12]

            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
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
    border_width = 0,
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

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
