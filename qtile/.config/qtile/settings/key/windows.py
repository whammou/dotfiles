from libqtile.config import EzKey, KeyChord, Key
from libqtile.lazy import lazy
from settings.layouts import hide_floating_win, show_floating_win

mod = "mod4"
alt = "mod1"
rofi_run_cmd = "rofi -show drun -m -1"


def hide_all_floating(qtile):
    group = qtile.current_group
    for window in group.windows:
        if window.floating:
            hide_floating_win(window)
            window.keep_below()


@lazy.window.function
def toggle_floating(window):
    window.disable_fullscreen()
    window.toggle_floating()
    show_floating_win(window)


@lazy.function
def floats_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.focus()
                window.bring_to_front()


@lazy.function
def floats_to_bottom(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.keep_below()
                hide_floating_win(window)


@lazy.window.function
def float_to_front(window):
    if window.floating:
        show_floating_win(window)
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


@lazy.group.function
def focus_back(group):
    history = group.focus_history
    if len(history) < 2:
        return
    target_window = history[-2]
    if target_window:
        group.focus(target_window)


@lazy.group.function
def focus_titling(group):
    group.focus(group.layout.last_focused_window)


@lazy.function
def pull_floating_to_tab(qtile):
    """Handle M-u for both floating and tiled windows.

    Floating windows are not in the Bonsai tree, so they must first be
    tiled via ``disable_floating()`` which triggers ``Group.mark_floating``
    -> ``Layout.add_client``. Then focus the newly tiled window and pull
    it out to a new tab at the nearest TabContainer.
    """
    win = qtile.current_window
    if win is not None and win.floating:
        try:
            win.disable_fullscreen()
        except Exception:
            pass
        win.disable_floating()
        group = qtile.current_group
        if group is not None:
            group.focus(win)
            layout = group.layout
            pane = getattr(layout, "focused_pane", None)
            tree = getattr(layout, "_tree", None)
            if pane is not None and tree is not None:
                try:
                    tree.pull_out_to_tab(pane, normalize=True)
                except ValueError:
                    return
                group.layout_all()
            else:
                func = getattr(layout, "pull_out_to_tab", None)
                if func is not None:
                    func()
    else:
        group = qtile.current_group
        if group is not None:
            layout = group.layout
            func = getattr(layout, "pull_out_to_tab", None)
            if func is not None:
                func()


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
        lazy.function(grow_window_maintain_aspect_ratio, 1.05).when(when_floating=True),
        lazy.window.center(),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4", "control"],
        "minus",
        lazy.function(grow_window_maintain_aspect_ratio, 0.95).when(when_floating=True),
        lazy.window.center(),
        desc="Shrink floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "equal",
        lazy.function(grow_window_maintain_aspect_ratio, 1.05).when(when_floating=True),
        desc="Grow floating window maintaining aspect ratio",
    ),
    Key(
        ["mod4"],
        "minus",
        lazy.function(grow_window_maintain_aspect_ratio, 0.95).when(when_floating=True),
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
    #     focus_next_floating_and_front(),
    #     desc="Focus next floating window",
    # ),
    # Key(
    #     [mod],
    #     "comma",
    #     focus_prev_floating_and_front(),
    #     desc="Focus previous floating window",
    # ),
    # Key(
    #     [mod, "Shift"],
    #     "comma",
    #     focus_prev_floating_and_front(),
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
        focus_prev_floating_and_front().when().when(when_floating=True),
    ),
    EzKey(
        "M-l",
        lazy.layout.right().when(when_floating=False),
        focus_prev_floating_and_front().when(when_floating=True),
    ),
    EzKey("M-k", lazy.layout.up()),
    EzKey("M-j", lazy.layout.down()),
    # Resize windows 3x
    EzKey("M-C-h", lazy.layout.resize("left", 300)),
    EzKey("M-C-l", lazy.layout.resize("right", 300)),
    EzKey("M-C-k", lazy.layout.resize("up", 150)),
    EzKey("M-C-j", lazy.layout.resize("down", 150)),
    # Swap tabs
    EzKey("A-S-b", lazy.layout.swap_tabs("previous")),
    EzKey("A-S-f", lazy.layout.swap_tabs("next")),
    # Select containers
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),
    # Windows States
    # EzKey("A-<Tab>", lazy.window.toggle_fullscreen()),
    # EzKey("M-<Tab>", focus_back()),
    EzKey("M-<grave>", lazy.function(toggle_tiling_floating_focus)),
    EzKey("M-C-<Escape>", lazy.group["scratchpad"].hide_all(), focus_titling()),
    EzKey(
        "M-<Escape>",
        lazy.function(toggle_tiling_floating_focus).when(when_floating=True),
    ),
    EzKey("M-S-C-<Escape>", lazy.group["scratchpad"].hide_all(), floats_to_bottom()),
    EzKey("M-f", lazy.window.toggle_fullscreen()),
    EzKey("M-<Tab>", toggle_floating()),
    # Floating Windows
    EzKey("A-S-0", floats_to_front()),
    # Rofi menu
    EzKey("M-S-w", lazy.spawn("rofi -show window")),
    EzKey("M-C-s", lazy.spawn(rofi_run_cmd)),
    # Container select mode
    KeyChord(
        ["mod4"],
        "w",
        [
            EzKey("M-v", lazy.layout.spawn_split(rofi_run_cmd, "x")),
            EzKey("M-x", lazy.layout.spawn_split(rofi_run_cmd, "y")),
            EzKey("M-t", lazy.layout.spawn_tab(rofi_run_cmd)),
            EzKey("M-S-t", lazy.layout.spawn_tab(rofi_run_cmd, new_level=True)),
            EzKey("M-w", lazy.layout.toggle_container_select_mode()),
            EzKey("M-h", lazy.layout.move_focus("left")),
            EzKey("M-j", lazy.layout.move_focus("down")),
            EzKey("M-k", lazy.layout.move_focus("up")),
            EzKey("M-l", lazy.layout.move_focus("right")),
            # Pull window out
            EzKey("M-o", lazy.layout.pull_out(position="next")),
            EzKey("S-o", lazy.layout.pull_out(position="previous")),
            EzKey("M-u", pull_floating_to_tab()),
            # Merge window to tab
            KeyChord(
                [mod],
                "m",
                [
                    EzKey("M-h", lazy.layout.merge_to_subtab("left")),
                    EzKey("M-l", lazy.layout.merge_to_subtab("right")),
                    EzKey("M-j", lazy.layout.merge_to_subtab("down")),
                    EzKey("M-k", lazy.layout.merge_to_subtab("up")),
                    EzKey(
                        "M-S-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.normalize(),
                    ),
                    EzKey(
                        "M-S-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.normalize(),
                    ),
                    EzKey(
                        "M-C-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.push_in("right", wrap=True),
                    ),
                    EzKey(
                        "M-A-h",
                        lazy.layout.merge_tabs("previous", "x"),
                        lazy.layout.push_in("left"),
                    ),
                    EzKey(
                        "M-C-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.push_in("right", wrap=True),
                    ),
                    EzKey(
                        "M-A-l",
                        lazy.layout.merge_tabs("next", "x"),
                        lazy.layout.push_in("left"),
                    ),
                ],
            ),
            # Push window in
            KeyChord(
                [mod],
                "i",
                [
                    EzKey("M-j", lazy.layout.push_in("down")),
                    EzKey("M-k", lazy.layout.push_in("up")),
                    EzKey("M-h", lazy.layout.push_in("left")),
                    EzKey("M-l", lazy.layout.push_in("right")),
                    EzKey(
                        "M-S-j",
                        lazy.layout.push_in("down", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "M-S-k",
                        lazy.layout.push_in("up", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "M-S-h",
                        lazy.layout.push_in("left", dest_selection="mru_deepest"),
                    ),
                    EzKey(
                        "M-S-l",
                        lazy.layout.push_in("right", dest_selection="mru_deepest"),
                    ),
                ],
            ),
        ],
    ),
]
