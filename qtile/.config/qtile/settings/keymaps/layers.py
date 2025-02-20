from libqtile.config import KeyChord, Key, EzKey
from libqtile.lazy import lazy



def focus_visible_window(mod, window_index, **spawn):
    keymaps =[]
    for i in window_index:
        keymaps.append(Key(mod, str(i), lazy.layout.focus_nth_window(i, **spawn)))
    return keymaps


def change_tab_layer(mod, tab_layer, tab_index):
    keymaps = []
    for tab in tab_layer:
        index_list = []
        for index in tab_index:
            index_list.append(EzKey(str(index), lazy.layout.focus_nth_tab(index, level=tab)))
        keymaps.append(KeyChord(mod, str(tab), index_list))
    return keymaps
