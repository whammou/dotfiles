from libqtile.config import KeyChord, Key, EzKey
from libqtile.lazy import lazy


def focus_visible_window(mod, window_index, **spawn):
    keymaps = []
    for i in window_index:
        keymaps.append(
            Key(
                mod,
                str(i),
                lazy.layout.focus_nth_window(i, **spawn),
                lazy.window.move_to_top(),
            )
        )
    return keymaps


def change_tab_layer(mod, tab_layer, tab_index):
    keymaps = []
    for tab in tab_layer:
        index_list = []
        for index in tab_index:
            index_list.append(
                EzKey(
                    str(index),
                    lazy.layout.focus_nth_tab(index, level=tab),
                    lazy.window.move_to_top(),
                )
            )
        keymaps.append(KeyChord(mod, str(tab), index_list))
    return keymaps


# FOCUS FLOATING WINDOW
@lazy.function
def focus_nth_floating_window(qtile, index):
    group = qtile.current_group
    floating_windows = [w for w in group.windows if w.floating]

    window_to_focus = floating_windows[index]

    window_to_focus.group.focus(window_to_focus)
    window_to_focus.move_to_top()


def focus_nth_floating(mod, index):
    key_list = []
    for i in index:
        key_list.append(
            Key(
                [], str(i), focus_nth_floating_window(i - 1), lazy.window.set_opacity(1)
            )
        )
    return [KeyChord(mod, "0", key_list)]
