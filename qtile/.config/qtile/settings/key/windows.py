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


@lazy.window.function
def float_to_front(window):
    if window.floating:
        window.bring_to_front()
        window.center()
    else:
        window.disable_floating()


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
    EzKey("A-S-d", lazy.layout.swap_tabs("previous")),
    EzKey("A-S-f", lazy.layout.swap_tabs("next")),
    # Select containers
    EzKey("M-o", lazy.layout.select_container_outer()),
    EzKey("M-i", lazy.layout.select_container_inner()),
    # Windows States
    EzKey("A-<Tab>", lazy.window.toggle_fullscreen()),
    EzKey("M-S-f", toggle_floating()),
    # Floating Windows
    EzKey("M-<Tab>", floats_to_front()),
    EzKey("C-A-f", lazy.window.move_up().when(when_floating=True)),
    EzKey("C-A-b", lazy.window.move_down().when(when_floating=True)),
    EzKey("M-d", lazy.group.prev_window()),
    EzKey("M-f", lazy.group.next_window()),
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
