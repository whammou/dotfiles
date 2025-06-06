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
                lazy.window.bring_to_front(),
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
                    lazy.window.bring_to_front(),
                )
            )
        keymaps.append(KeyChord(mod, str(tab), index_list))
    return keymaps


@lazy.function
def focus_nth_floating_window(qtile, index):
    group = qtile.current_group
    floating_windows = [w for w in group.windows if w.floating]

    window_to_focus = floating_windows[index]

    window_to_focus.group.focus(window_to_focus)
    window_to_focus.bring_to_front()


def focus_nth_floating(mod, index):
    key_list = []
    for i in index:
        key_list.append(Key([], str(i + 1), focus_nth_floating_window(i)))
    return [KeyChord(mod, "0", key_list)]
