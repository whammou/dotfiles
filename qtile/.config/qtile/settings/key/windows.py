from libqtile.config import EzKey, KeyChord, Key
from libqtile.lazy import lazy

mod = "mod4"
alt = "mod1"
rofi_run_cmd = "rofi -show drun -m -1"


windows_keys = [
    EzKey("M-m", lazy.window.keep_below()),
    # Swap Windows
    EzKey(
        "M-S-h",
        lazy.layout.swap("left").when(when_floating=False),
        lazy.window.move_floating(-32, 0).when(when_floating=True),
    ),
    EzKey(
        "M-S-l",
        lazy.layout.swap("right").when(when_floating=False),
        lazy.window.move_floating(+32, 0).when(when_floating=True),
    ),
    EzKey(
        "M-S-k",
        lazy.layout.swap("up").when(when_floating=False),
        lazy.window.move_floating(0, -18).when(when_floating=True),
    ),
    EzKey(
        "M-S-j",
        lazy.layout.swap("down").when(when_floating=False),
        lazy.window.move_floating(0, +18).when(when_floating=True),
    ),
    Key(
        ["mod4", "control"],
        "equal",
        lazy.layout.grow_window_maintain_aspect_ratio(1.05).when(when_floating=True),
        lazy.window.center(),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4", "control"],
        "minus",
        lazy.layout.grow_window_maintain_aspect_ratio(0.95).when(when_floating=True),
        lazy.window.center(),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "equal",
        lazy.layout.grow_window_maintain_aspect_ratio(1.05).when(when_floating=True),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "minus",
        lazy.layout.grow_window_maintain_aspect_ratio(0.95).when(when_floating=True),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4", "Shift"],
        "equal",
        lazy.window.center(),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    # Key(
    #     [mod],
    #     "period",
    #     lazy.layout.focus_next_floating(),
    #     desc="Focus next floating window",
    # ),
    # Key(
    #     [mod],
    #     "comma",
    #     lazy.layout.focus_prev_floating(),
    #     desc="Focus previous floating window",
    # ),
    # Key(
    #     [mod, "Shift"],
    #     "comma",
    #     lazy.layout.focus_prev_floating(),
    #     desc="Focus previous floating window",
    # ),
    # Resize windows
    # EzKey("M-C-h", lazy.layout.resize("left", 100)),
    # EzKey("M-C-l", lazy.layout.resize("right", 100)),
    # EzKey("M-C-k", lazy.layout.resize("up", 100)),
    # EzKey("M-C-j", lazy.layout.resize("down", 100)),
    # Navigate
    EzKey(
        "M-h",
        lazy.layout.left().when(when_floating=False),
        lazy.layout.focus_prev_floating().when(when_floating=True),
    ),
    EzKey(
        "M-l",
        lazy.layout.right().when(when_floating=False),
        lazy.layout.focus_next_floating().when(when_floating=True),
    ),
    EzKey("M-k", lazy.layout.up()),
    EzKey("M-j", lazy.layout.down()),
    # Resize windows 3x
    EzKey("M-C-h", lazy.layout.resize("left", 300)),
    EzKey("M-C-l", lazy.layout.resize("right", 300)),
    EzKey("M-C-k", lazy.layout.resize("up", 150)),
    EzKey("M-C-j", lazy.layout.resize("down", 150)),
    # Swap tabs — brackets must use keysym names bracketleft/bracketright
    # EzKey parses "<bracketleft>" → "bracketleft" (keysyms["bracketleft"]=91), while "[" is NOT a valid keysym
    EzKey("M-<bracketleft>", lazy.layout.swap_tabs("previous")),
    EzKey("M-<bracketright>", lazy.layout.swap_tabs("next")),
    # Select containers
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),
    # Windows States
    # EzKey("A-<Tab>", lazy.window.toggle_fullscreen()),
    # EzKey("M-<Tab>", focus_back()),
    EzKey("M-S-<grave>", lazy.layout.toggle_tiling_floating_focus()),
    EzKey(
        "M-<Escape>",
        lazy.layout.toggle_tiling_floating_focus().when(when_floating=True),
    ),
    EzKey("M-S-C-<Escape>", lazy.group["scratchpad"].hide_all(), lazy.layout.floats_to_bottom()),
    EzKey("M-f", lazy.window.toggle_fullscreen()),
    EzKey("M-<Tab>", lazy.layout.toggle_floating()),
    EzKey("M-S-<Tab>", lazy.layout.pull_floating_to_tab()),
    EzKey("A-S-0", lazy.layout.floats_to_front()),
    # Rofi menu
    # EzKey("M-S-w", lazy.spawn("rofi -show window")),  # temporarily disabled for WindowName toggle
    EzKey("M-S-w", lazy.widget["windowname_box"].toggle(), desc="Toggle WindowName"),
    EzKey("M-C-s", lazy.spawn(rofi_run_cmd)),
    EzKey(
        "M-C-w",
        lazy.layout.spawn("wlr-which-key ops.yaml"),
        desc="Window ops menu",
    ),
    # Container select mode
    KeyChord(
        ["mod4"],
        "w",
        [
            EzKey("v", lazy.layout.spawn_split(rofi_run_cmd, "x")),
            EzKey("x", lazy.layout.spawn_split(rofi_run_cmd, "y")),
            EzKey("t", lazy.layout.spawn_tab(rofi_run_cmd)),
            EzKey("S-t", lazy.layout.spawn_tab(rofi_run_cmd, new_level=True)),
            EzKey("w", lazy.layout.toggle_container_select_mode()),
            EzKey("h", lazy.layout.move_focus("left")),
            EzKey("j", lazy.layout.move_focus("down")),
            EzKey("k", lazy.layout.move_focus("up")),
            EzKey("l", lazy.layout.move_focus("right")),
            # Pull window out
            EzKey("o", lazy.layout.pull_out(position="next")),
            EzKey("S-o", lazy.layout.pull_out(position="previous")),
            EzKey("u", lazy.layout.pull_floating_to_tab()),
            # Merge window to tab
            KeyChord(
                [],
                "m",
                [
                    EzKey("h", lazy.layout.merge_to_subtab("left")),
                    EzKey("l", lazy.layout.merge_to_subtab("right")),
                    EzKey("j", lazy.layout.merge_to_subtab("down")),
                    EzKey("M-k", lazy.layout.merge_to_subtab("up")),
                    EzKey(
                        "S-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.normalize(),
                    ),
                    EzKey(
                        "S-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.normalize(),
                    ),
                    EzKey(
                        "C-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.push_in("right", wrap=True),
                    ),
                    EzKey(
                        "A-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.push_in("left"),
                    ),
                    EzKey(
                        "C-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.push_in("right", wrap=True),
                    ),
                    EzKey(
                        "A-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.push_in("left"),
                    ),
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
        ],
    ),
]
