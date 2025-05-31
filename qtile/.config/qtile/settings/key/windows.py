from libqtile.config import EzKey, KeyChord
from libqtile.lazy import lazy


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


@lazy.window.function
def float_to_front(window):
    if window.floating:
        window.bring_to_front()
        window.center()
    else:
        window.disable_floating()


@lazy.window.function
def resize_floating_window(window, width: int = 0, height: int = 0):
    window.set_size_floating(window.width + width, window.height + height)


@lazy.window.function
def move_floating_window(window, x: int = 0, y: int = 0):
    window.set_position_floating(window.float_x + x, window.float_y + y)


windows_keys = [
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
    EzKey("A-<Tab>", lazy.window.toggle_fullscreen()),
    EzKey("M-<Escape>", lazy.group["scratchpad"].hide_all()),
    EzKey("M-S-<Escape>", floats_keep_below()),
    EzKey("M-S-f", toggle_floating()),
    # Floating Windows
    EzKey("A-0", floats_to_front()),
    EzKey(
        "M-d",
        lazy.group.prev_window(),
        lazy.window.bring_to_front().when(when_floating=True),
    ),
    EzKey(
        "M-u",
        lazy.group.next_window(),
        lazy.window.bring_to_front().when(when_floating=True),
    ),
    EzKey("M-C-u", resize_floating_window(width=-100, height=-100)),
    EzKey("M-C-d", resize_floating_window(width=100, height=100)),
    # Rofi menu
    EzKey("M-S-w", lazy.spawn("rofi -show window")),
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
