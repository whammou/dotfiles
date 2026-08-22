from libqtile.config import KeyChord, Key, EzKey
from libqtile.lazy import lazy
from qtile_bonsai import Bonsai

from .windows import hide_all_floating


def focus_visible_window(mod, window_index, **spawn):
    keymaps = []
    for i in window_index:
        keymaps.append(
            Key(
                mod,
                str(i),
                lazy.layout.focus_nth_window(i, **spawn),
                # lazy.window.bring_to_front(),
                # lazy.function(hide_all_floating),
            )
        )
    return keymaps


@lazy.function
def focus_nth_tab_keep_floating(qtile, n: int, level: int):
    """Switch bonsai tab without losing focus on floating window.

    If current window is floating, suppress hide_floating_win and restore
    focus after Bonsai's _request_focus (mirrors maintain_focus pattern in
    settings/layouts.py).
    """
    group = qtile.current_group
    cur = qtile.current_window
    layout = group.layout

    if not isinstance(layout, Bonsai) or cur is None or not cur.floating:
        if isinstance(layout, Bonsai):
            layout.focus_nth_tab(n, level=level)
        return

    import settings.layouts as L

    L._suppress_floating_hide = True
    layout.focus_nth_tab(n, level=level)

    def _restore():
        if cur.group is not None:
            group.focus(cur)
            cur.bring_to_front()
            L.show_floating_win(cur)

    qtile.call_soon(_restore)


def change_tab_layer(mod, tab_layer, tab_index):
    keymaps = []
    for tab in tab_layer:
        index_list = []
        for index in tab_index:
            index_list.append(
                EzKey(
                    str(index),
                    focus_nth_tab_keep_floating(index, level=tab),
                )
            )
        keymaps.append(KeyChord(mod, str(tab), index_list))
    return keymaps


# FOCUS FLOATING WINDOW
@lazy.function
def focus_nth_floating_window(qtile, index):
    group = qtile.current_group
    floating_windows = [w for w in group.windows if w.floating]

    try:
        window_to_focus = floating_windows[index]
        window_to_focus.group.focus(window_to_focus)
        window_to_focus.bring_to_front()
    except IndexError:
        # This block runs only if the index is out of range.
        # 'pass' means "do nothing".
        pass


def focus_nth_floating(mod, index):
    key_list = []
    for i in index:
        key_list.append(
            Key([], str(i), focus_nth_floating_window(i - 1), lazy.window.center())
        )
    return [KeyChord(mod, "0", key_list)]
