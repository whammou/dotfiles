from libqtile.config import KeyChord, Key, EzKey
from libqtile.lazy import lazy


mod = "mod4"
meta = "mod1"


def focus_visible_window(window_index):
    keymaps =[]
    for i in window_index:
        keymaps.append(Key([meta], str(i), lazy.layout.focus_nth_window(i, ignore_inactive_tabs_at_levels=[1,2])))
    return keymaps


def change_tab_layer(tab_layer, tab_index):
    keymaps = []
    for tab in tab_layer:
        index_list = []
        for index in tab_index:
            index_list.append(EzKey(str(index), lazy.layout.focus_nth_tab(index, level=tab)))
        keymaps.append(KeyChord([mod], str(tab), index_list))
    return keymaps
