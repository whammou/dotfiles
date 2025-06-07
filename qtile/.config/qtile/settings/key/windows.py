from libqtile.config import EzKey, KeyChord, Key
from libqtile.lazy import lazy

mod = "mod4"
alt = "mod1"


@lazy.window.function
def toggle_floating(window):
    window.toggle_floating()
    window.center()


@lazy.function
def floats_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.focus()
                window.bring_to_front()


@lazy.function
def floats_keep_below(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.keep_below()
                window.set_opacity(0)


@lazy.window.function
def float_to_front(window):
    if window.floating:
        window.bring_to_front()
        window.center()
    else:
        window.disable_floating()


def grow_window_maintain_aspect_ratio(qtile, factor):
    win = qtile.current_window
    w, h = (
        win.info()["width"],
        win.info()["height"],
    )

    new_w = int(w * factor)
    new_h = int(h * factor)

    win.set_size_floating(new_w, new_h)


def move_floating_window(qtile, x_increment, y_increment):
    win = qtile.current_window
    x, y = (
        win.info()["x"],
        win.info()["y"],
    )

    new_x = int(x + x_increment)
    new_y = int(y + y_increment)

    win.set_position_floating(new_x, new_y)


@lazy.function
def focus_next_floating_and_front(qtile):
    group = qtile.current_group
    floating_windows = [w for w in group.windows if w.floating]

    if not floating_windows:
        return

    current_focused = qtile.current_window
    window_to_focus = None

    if current_focused and current_focused.floating:
        try:
            current_index = floating_windows.index(current_focused)
            next_index = (current_index + 1) % len(floating_windows)
            window_to_focus = floating_windows[next_index]
        except ValueError:
            # Current window not in floating_windows (e.g., it was just made floating)
            window_to_focus = floating_windows[0]
    elif floating_windows:
        # If currently focused is tiled, focus the first floating window
        window_to_focus = floating_windows[0]

    if window_to_focus:
        window_to_focus.group.focus(window_to_focus)


@lazy.function
def focus_prev_floating_and_front(qtile):
    group = qtile.current_group
    floating_windows = [w for w in group.windows if w.floating]

    if not floating_windows:
        return

    current_focused = qtile.current_window
    window_to_focus = None

    if current_focused and current_focused.floating:
        try:
            current_index = floating_windows.index(current_focused)
            prev_index = (current_index - 1 + len(floating_windows)) % len(
                floating_windows
            )
            window_to_focus = floating_windows[prev_index]
        except ValueError:
            window_to_focus = floating_windows[-1]
    elif floating_windows:
        window_to_focus = floating_windows[-1]

    if window_to_focus:
        window_to_focus.group.focus(window_to_focus)


def toggle_tiling_floating_focus(qtile):
    current_group = qtile.current_group
    if not current_group:
        return

    last_tiling = None
    last_floating = None

    # Iterate through the focus history to find the most recent of each type
    for window in reversed(current_group.focus_history):
        if window not in current_group.windows:
            continue
        if window.floating and not last_floating:
            last_floating = window
        elif not window.floating and not last_tiling:
            last_tiling = window
        # Stop searching once both are found
        if last_tiling and last_floating:
            break

    # Decide which window to focus
    if not last_tiling and not last_floating:
        return  # No valid windows to switch between

    target_window = None
    # If currently on the last tiling window, switch to floating
    if qtile.current_window == last_tiling and last_floating:
        target_window = last_floating
    # Otherwise, switch to the last tiling window (or if it's the only one available)
    elif last_tiling:
        target_window = last_tiling
    # Fallback to floating if tiling doesn't exist
    elif last_floating:
        target_window = last_floating

    # Focus the target window if it's not already focused
    if target_window and qtile.current_window != target_window:
        current_group.focus(target_window)
        target_window.bring_to_front()


windows_keys = [
    Key(
        [alt],
        "Tab",
        lazy.function(toggle_tiling_floating_focus),
        lazy.window.set_opacity(1),
        desc="Focus latest focused floating window",
    ),
    EzKey("M-h", lazy.function(move_floating_window, -32, 0).when(when_floating=True)),
    EzKey("M-l", lazy.function(move_floating_window, +32, 0).when(when_floating=True)),
    EzKey("M-k", lazy.function(move_floating_window, 0, -18).when(when_floating=True)),
    EzKey("M-j", lazy.function(move_floating_window, 0, +18).when(when_floating=True)),
    Key(
        ["mod4", "control"],
        "equal",
        lazy.function(grow_window_maintain_aspect_ratio, 1.05).when(when_floating=True),
        lazy.window.center(),
        lazy.window.bring_to_front(),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4", "control"],
        "minus",
        lazy.function(grow_window_maintain_aspect_ratio, 0.95).when(when_floating=True),
        lazy.window.center(),
        lazy.window.bring_to_front(),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "equal",
        lazy.function(grow_window_maintain_aspect_ratio, 1.1).when(when_floating=True),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "minus",
        lazy.function(grow_window_maintain_aspect_ratio, 0.9).when(when_floating=True),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    Key(
        [mod],
        "period",
        focus_next_floating_and_front(),
        lazy.window.bring_to_front(),
        desc="Focus next floating window",
    ),
    Key(
        [mod],
        "comma",
        focus_prev_floating_and_front(),
        lazy.window.bring_to_front(),
        desc="Focus previous floating window",
    ),
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
    # Swap tabs
    EzKey("A-S-b", lazy.layout.swap_tabs("previous")),
    EzKey("A-S-f", lazy.layout.swap_tabs("next")),
    # Select containers
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),
    # Windows States
    # EzKey("A-<Tab>", lazy.window.toggle_fullscreen()),
    EzKey(
        "M-<Escape>",
        lazy.window.keep_below().when(when_floating=True),
        lazy.window.set_opacity(0.0).when(when_floating=True),
    ),
    EzKey("M-C-<Escape>", lazy.group["scratchpad"].hide_all()),
    EzKey(
        "M-S-<Escape>",
        floats_keep_below(),
        lazy.window.set_opacity(0).when(when_floating=True),
    ),
    EzKey("M-S-C-<Escape>", lazy.group["scratchpad"].hide_all(), floats_keep_below()),
    # EzKey("M-<Escape>", floats_keep_below()),
    EzKey("M-S-f", toggle_floating()),
    # Floating Windows
    EzKey("A-S-0", floats_to_front()),
    # EzKey("M-C-u", resize_floating_window(width=-10, height=-10), lazy.window.center()),
    # EzKey("M-C-d", resize_floating_window(width=10, height=10), lazy.window.center()),
    # Rofi menu
    EzKey("M-S-w", lazy.spawn("rofi -show window")),
    #    EzKey(
    #        "M-d",
    #        lazy.group.prev_window(),
    #        lazy.window.bring_to_front().when(when_floating=True),
    #    ),
    #    EzKey(
    #        "M-u",
    #        lazy.group.next_window(),
    #        lazy.window.bring_to_front().when(when_floating=True),
    #    ),
    # Container select mode
    KeyChord(
        ["mod4"],
        "w",
        [
            EzKey("C-v", lazy.layout.toggle_container_select_mode()),
            # Pull window out
            EzKey("o", lazy.layout.pull_out(position="next")),
            EzKey("S-o", lazy.layout.pull_out(position="previous")),
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
                    EzKey("S-h", lazy.layout.merge_tabs("previous", "x")),
                    EzKey("S-l", lazy.layout.merge_tabs("next", "x")),
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
