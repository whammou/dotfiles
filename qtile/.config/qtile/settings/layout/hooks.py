# Layout-related hook subscriptions.
#
# Split from settings/layouts.py — handlers only. Shared window helpers
# and geometry state live in .commands and are imported below.
# Importing this module registers all hooks via @hook.subscribe.

from libqtile import hook, qtile

from .commands import (
    _forget_all,
    _hide_all_in_group,
    _is_focus_allowed,
    _is_visible,
    hide_floating_win,
    show_floating_win,
)

_last_focused = None
_suppress_floating_hide = False
_floating_sound_startup = True


@hook.subscribe.client_new
def hide_floating_new(win):
    if _is_focus_allowed(win):
        grp = getattr(win, "group", None)
        if grp is not None:
            _hide_all_in_group(grp, exclude=win)
        return
    grp = getattr(win, "group", None)
    if grp is not None:
        _hide_all_in_group(grp)
    hide_floating_win(win)


@hook.subscribe.client_managed
def hide_floating(win):
    if _is_focus_allowed(win):
        grp = getattr(win, "group", None) or getattr(qtile, "current_group", None)
        if grp is not None:
            _hide_all_in_group(grp, exclude=win)
        show_floating_win(win)
        try:
            cur = getattr(qtile, "current_group", None)
            if grp is not None and grp is cur:
                grp.focus(win, warp=False)
        except Exception:
            pass
        return
    grp = getattr(win, "group", None) or getattr(qtile, "current_group", None)
    if grp is not None:
        _hide_all_in_group(grp)
    hide_floating_win(win)


@hook.subscribe.group_window_add
def hide_floating_on_group_add(group, window):
    if _is_focus_allowed(window):
        _hide_all_in_group(group, exclude=window)
        show_floating_win(window)
        return
    _hide_all_in_group(group)
    if getattr(window, "floating", False):
        hide_floating_win(window)


@hook.subscribe.startup_complete
def _disable_floating_sound_startup():
    global _floating_sound_startup
    _floating_sound_startup = False


@hook.subscribe.client_managed
def play_floating_sound(window):
    global _floating_sound_startup
    if _floating_sound_startup or not getattr(window, "floating", False):
        return
    import os

    sound = os.path.expanduser("~/.local/share/bell/staplebops-05.wav")
    qtile.spawn(f"pw-play --media-role=Notification --volume=1.0 {sound}")


@hook.subscribe.client_focus
def on_client_focus(window):
    global _last_focused, _suppress_floating_hide
    grp = getattr(window, "group", None) or getattr(qtile, "current_group", None)
    _hide_all_in_group(grp, exclude=window)
    if (
        _last_focused is not None
        and _last_focused is not window
        and getattr(_last_focused, "floating", False)
        and not _suppress_floating_hide
        and _is_visible(_last_focused)
    ):
        hide_floating_win(_last_focused)
    if getattr(window, "floating", False) and _is_visible(window):
        try:
            window.bring_to_front()
        except Exception:
            pass
    _last_focused = window
    _suppress_floating_hide = False


@hook.subscribe.client_killed
def _cleanup_hidden_on_killed(window):
    _forget_all(getattr(window, "wid", None))


@hook.subscribe.group_window_remove
def _cleanup_hidden_on_remove(group, window):
    _forget_all(getattr(window, "wid", None))


@hook.subscribe.group_window_add
def no_focus_steal(group, window):
    prev = group.current_window
    if prev is None:
        return
    if _is_focus_allowed(window):
        return
    window.can_steal_focus = False
    qtile_inst = getattr(group, "qtile", None)
    if qtile_inst:

        def _reclaim():
            if (
                getattr(window, "floating", False)
                and window.group is group
                and prev.group is group
            ):
                group.focus(prev, warp=False)

        qtile_inst.call_soon(_reclaim)


@hook.subscribe.group_window_remove
def after_killed_focus_same_L1(group, window):
    try:
        if window not in group.focus_history:
            group.focus_history.append(window)
    except Exception:
        pass
    from qtile_bonsai import Bonsai
    from qtile_bonsai.core.nodes import Tab

    layout = group.layout
    if not isinstance(layout, Bonsai) or layout._tree.is_empty:
        return
    try:
        qtile_inst = getattr(group, "qtile", None)
        is_floating = bool(getattr(window, "floating", False))
        killed_L1 = None
        try:
            pane = layout._windows_to_panes.get(window) if not is_floating else None
            base = pane or layout.focused_pane
            if base is None:
                try:
                    base = next(layout._tree.iter_panes())
                except StopIteration:
                    base = None
            if base is not None:
                tabs = list(reversed(base.get_ancestors(Tab)))
                if tabs:
                    killed_L1 = tabs[0]
        except Exception:
            killed_L1 = None

        if is_floating:
            removed = []
            try:
                idx = group.focus_history.index(window)
                i = idx - 1
                while i >= 0 and getattr(group.focus_history[i], "floating", False):
                    removed.append(group.focus_history[i])
                    i -= 1
                for w in removed:
                    try:
                        group.focus_history.remove(w)
                    except ValueError:
                        pass
                if removed and qtile_inst:

                    def _reinsert():
                        for w in removed:
                            if w not in group.focus_history and w in group.windows:
                                group.focus_history.append(w)

                    qtile_inst.call_soon(_reinsert)
            except (ValueError, IndexError, AttributeError):
                pass

        def _restore():
            if group.current_window is window:
                return
            try:
                target_tab = killed_L1
                if target_tab is None or target_tab not in list(
                    layout._tree.iter_walk()
                ):
                    cur_pane = layout.focused_pane
                    if cur_pane is None:
                        try:
                            cur_pane = next(layout._tree.iter_panes())
                        except StopIteration:
                            return
                    tabs = list(reversed(cur_pane.get_ancestors(Tab)))
                    if not tabs:
                        return
                    target_tab = tabs[0]
                target_pane = layout._tree.find_mru_pane(start_node=target_tab)
                target = getattr(target_pane, "window", None) if target_pane else None
                if (
                    target
                    and not target.floating
                    and target.group is group
                    and group.current_window is not target
                ):
                    group.focus(target, warp=False)
            except Exception:
                return

        if qtile_inst:
            qtile_inst.call_soon(_restore)
        _restore()
    except Exception:
        return


@hook.subscribe.client_killed
def clean_ghost_panes(window):
    try:
        all_groups = getattr(qtile, "groups", []) or []
        qt_inst = (
            getattr(window, "qtile", None) or getattr(qtile, "qtile", None) or qtile
        )

        def _clean():
            for grp in list(all_groups):
                lay = getattr(grp, "layout", None)
                from qtile_bonsai import Bonsai as _B

                if not isinstance(lay, _B):
                    continue
                ghosts = []
                try:
                    live_panes = set(lay._tree.iter_panes())
                    for win, pane in list(lay._windows_to_panes.items()):
                        if (
                            pane not in live_panes
                            or getattr(pane, "window", None) is None
                            or getattr(pane, "window", None) not in grp.windows
                        ):
                            ghosts.append((win, pane))
                    for pane in list(lay._tree.iter_panes()):
                        if getattr(pane, "window", None) is None:
                            for win, p in list(lay._windows_to_panes.items()):
                                if p is pane:
                                    ghosts.append((win, pane))
                                    break
                            else:
                                try:
                                    lay._tree.remove(pane, normalize=True)
                                except Exception:
                                    pass
                except Exception:
                    continue
                for win, pane in ghosts:
                    try:
                        if pane in set(lay._tree.iter_walk()):
                            try:
                                lay._tree.remove(pane, normalize=True)
                            except Exception:
                                pass
                    except Exception:
                        pass
                    try:
                        if win in lay._windows_to_panes:
                            del lay._windows_to_panes[win]
                    except Exception:
                        pass
                if ghosts:
                    try:
                        lay._request_relayout()
                    except Exception:
                        pass
                    try:
                        grp.layout_all()
                    except Exception:
                        pass

        _clean()
        try:
            if qt_inst:
                qt_inst.call_soon(_clean)
        except Exception:
            pass
    except Exception:
        pass
