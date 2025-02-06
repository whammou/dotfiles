from libqtile.config import Key, EzKey, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from .keymaps.motions import focus_visible_window, change_bonsai_tab_layer

terminal = guess_terminal()
mod = "mod4"

keys = [

    # Utilities keybindings
    Key([mod, 'Shift'], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    # Spawn position
    EzKey("M-x", lazy.layout.spawn_split(terminal, "x")),
    EzKey("M-y", lazy.layout.spawn_split(terminal, "y")),
    EzKey("M-t", lazy.layout.spawn_tab(terminal)),
    EzKey("M-S-t", lazy.layout.spawn_tab(terminal, new_level=True)),

    EzKey("M-S-v", lazy.layout.spawn_split(terminal, "x", position="previous")),
    EzKey("M-S-x", lazy.layout.spawn_split(terminal, "y", position="previous")),


    # Resize windows
    EzKey("M-C-h", lazy.layout.resize("left", 100)),
    EzKey("M-C-l", lazy.layout.resize("right", 100)),
    EzKey("M-C-k", lazy.layout.resize("up", 100)),
    EzKey("M-C-j", lazy.layout.resize("down", 100)),

    # Swap Windows
    EzKey("M-S-h", lazy.layout.swap("left")),
    EzKey("M-S-l", lazy.layout.swap("right")),
    EzKey("M-S-k", lazy.layout.swap("up")),
    EzKey("M-S-j", lazy.layout.swap("down")),
    EzKey("A-S-d", lazy.layout.swap_tabs("previous")),
    EzKey("A-S-f", lazy.layout.swap_tabs("next")),

    #Select containers
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),

    # Container select mode
    KeyChord(
        ["mod4"],
        "w",
        [
            EzKey("C-v", lazy.layout.toggle_container_select_mode()),

            # Pull window out
            EzKey("o", lazy.layout.pull_out()),
            EzKey("u", lazy.layout.pull_out_to_tab()),

            # Merge window to tab
            KeyChord(
                [],
                "m",
                [
                    EzKey("h", lazy.layout.merge_to_subtab("left")),
                    EzKey("l", lazy.layout.merge_to_subtab("right")),
                    EzKey("j", lazy.layout.merge_to_subtab("down")),
                    EzKey("k", lazy.layout.merge_to_subtab("up")),

                    EzKey("S-h", lazy.layout.merge_tabs("previous")),
                    EzKey("S-l", lazy.layout.merge_tabs("next")),
                ],
            ),
 
            # Push window in
            KeyChord(
                [],
                "i",
                [
                    EzKey("j", lazy.layout.push_in("down")),
                    EzKey("k", lazy.layout.push_in("up")),
                    EzKey("h", lazy.layout.push_in("left")),
                    EzKey("l", lazy.layout.push_in("right")),
 
                    EzKey("S-j", lazy.layout.push_in("down", dest_selection="mru_deepest"),),
                    EzKey("S-k", lazy.layout.push_in("up", dest_selection="mru_deepest"),),
                    EzKey("S-h", lazy.layout.push_in("left", dest_selection="mru_deepest"),),
                    EzKey("S-l", lazy.layout.push_in("right", dest_selection="mru_deepest"),),
                ],
            ),
        ]
    ),
]

keys = keys + focus_visible_window(9) + change_bonsai_tab_layer(9, 9)
