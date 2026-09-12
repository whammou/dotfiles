from libqtile import hook, layout, qtile
from libqtile.config import Match

from .layout.custom_bonsai import SmartBonsai
from .screens import GAP
from .theme import colors
from .smart_bonsai import smart_split

_last_focused = None
_suppress_floating_hide = False
_floating_sound_startup = True

_hidden_geoms: dict[int, tuple[int, int, int, int]] = {}
_last_toggle_geoms: dict[int, tuple[int, int, int, int]] = {}


def _is_visible(win) -> bool:
    return not bool(getattr(win, "hidden", False) or getattr(win, "minimized", False))


def _save_geom(win) -> None:
    wid = getattr(win, "wid", None)
    if wid is None:
        return
    try:
        w, h, x, y = int(win.width), int(win.height), int(win.x), int(win.y)
        if w > 0 and h > 0:
            cur = (x, y, w, h)
            if _hidden_geoms.get(wid) != cur:
                _hidden_geoms[wid] = cur
    except Exception:
        pass


def _hide_all_in_group(group, exclude=None) -> None:
    if group is None:
        return
    for w in list(getattr(group, "windows", [])):
        if w is exclude or getattr(w, "fullscreen", False) or not getattr(w, "floating", False):
            continue
        if _is_visible(w):
            hide_floating_win(w)


def _forget(wid: int | None) -> None:
    if wid is not None:
        _hidden_geoms.pop(wid, None)


def _forget_toggle(wid: int | None) -> None:
    if wid is not None:
        _last_toggle_geoms.pop(wid, None)


def _forget_all(wid: int | None) -> None:
    if wid is not None:
        _hidden_geoms.pop(wid, None)
        _last_toggle_geoms.pop(wid, None)


def _remember_toggle_geom(win) -> None:
    wid = getattr(win, "wid", None)
    if wid is None:
        return
    try:
        w, h, x, y = int(win.width), int(win.height), int(win.x), int(win.y)
        if w > 0 and h > 0:
            _last_toggle_geoms[wid] = (x, y, w, h)
    except Exception:
        pass


def _restore_toggle_geom(win) -> bool:
    wid = getattr(win, "wid", None)
    geom = _last_toggle_geoms.get(wid) if wid is not None else None
    if geom is not None:
        try:
            x, y, w, h = geom
            win.place(x, y, w, h, win.borderwidth, win.bordercolor, above=False, respect_hints=False)
            try:
                win.bring_to_front()
            except Exception:
                pass
            return True
        except Exception:
            pass
    try:
        win.center()
    except Exception:
        pass
    return False


def hide_floating_win(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    _save_geom(win)
    if not _is_visible(win):
        return
    try:
        if hasattr(win, "hide"):
            win.hide()
        elif hasattr(win, "minimized"):
            win.minimized = True  # type: ignore[attr-defined]
    except (AttributeError, RuntimeError):
        pass


def show_floating_win(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    if _is_visible(win):
        try:
            win.bring_to_front()
        except Exception:
            pass
        return
    wid = getattr(win, "wid", None)
    geom = _hidden_geoms.pop(wid, None) if wid is not None else None
    try:
        if hasattr(win, "unhide"):
            win.unhide()
        elif hasattr(win, "minimized"):
            win.minimized = False  # type: ignore[attr-defined]
    except (AttributeError, RuntimeError):
        pass
    if geom is not None:
        try:
            x, y, w, h = geom
            win.place(x, y, w, h, win.borderwidth, win.bordercolor, above=False, respect_hints=False)
        except Exception:
            pass
    try:
        win.bring_to_front()
    except Exception:
        pass


def toggle_floating_minimize(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    hide_floating_win(win) if _is_visible(win) else show_floating_win(win)


def is_floating_hidden(win) -> bool:
    return bool(getattr(win, "floating", False) and not _is_visible(win))


@hook.subscribe.client_new
def hide_floating_new(win):
    grp = getattr(win, "group", None)
    if grp is not None:
        _hide_all_in_group(grp)
    hide_floating_win(win)


@hook.subscribe.client_managed
def hide_floating(win):
    grp = getattr(win, "group", None) or getattr(qtile, "current_group", None)
    if grp is not None:
        _hide_all_in_group(grp)
    hide_floating_win(win)


@hook.subscribe.group_window_add
def hide_floating_on_group_add(group, window):
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
    window.can_steal_focus = False
    qtile_inst = getattr(group, "qtile", None)
    if qtile_inst:

        def _reclaim():
            if getattr(window, "floating", False) and window.group is group and prev.group is group:
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
                if target_tab is None or target_tab not in list(layout._tree.iter_walk()):
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
                if target and not target.floating and target.group is group and group.current_window is not target:
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
        qt_inst = getattr(window, "qtile", None) or getattr(qtile, "qtile", None) or qtile

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
                        if pane not in live_panes or getattr(pane, "window", None) is None or getattr(pane, "window", None) not in grp.windows:
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


BORDER_WIDTH = 3
BORDER_COLOR = colors["grey"]

layouts = [
    SmartBonsai(
        **{
            "auto_cwd_for_terminals": False,
            "window.border_size": BORDER_WIDTH,
            "window.single.border_size": BORDER_WIDTH,
            "window.border_color": colors["bg0"],
            "window.active.border_color": BORDER_COLOR,
            "window.margin": [0, GAP, GAP * 2, GAP],
            "window.default_add_mode": smart_split,
            "excluded_wm_classes": [],
            "float_sizes": {
                "org-agenda": "pad_large",
                "org-backlog": "pad_large",
                "org-browse": "pad_large",
                "org-super-agenda": "pad_large",
                "org-search": "pad_large",
                "lazygit-journal": "pad_large",
                "lazygit-dotfiles": "pad_large",
                "org-capture": "pad_small",
                "org-roam-capture": "pad_small",
                "nvim": "pad_large",
                "opencode": "pad_small",
                "opencode-attach": "pad_small",
                "test-session": "pad_extra_large",
                "yazi": "pad_medium",
                "yazi-sftp": "pad_medium",
                "yazi-journal": "pad_large",
                "tmux-session": "pad_large",
                "ssh-session": "pad_large",
                "btm": "pad_medium",
                "mon-battery": "pad_list",
                "mon-voltage": "pad_list",
                "tlp-recalibrate": "pad_list",
                "watch-cpu": "pad_list",
                "nvtop": "pad_medium",
                "ncdu": "pad_medium",
                "xset": "pad_small",
                "sysz-user": "pad_medium",
                "sysz-system": "pad_medium",
                "fzf-emoji": "pad_small",
                "bluetuith": "pad_small",
                "yt-x": "pad_small",
                "sys-upgrade": "pad_large",
                "chessterm": "pad_small",
                "newsboat": "pad_large",
                "notif-history": "pad_small",
                "neomutt": "pad_large",
                "mangal": "pad_small",
                "dict": "pad_small",
                "anifzf": "pad_small",
                "ani-cli": "pad_small",
                "typing-test": "pad_typing",
                "kari": "pad_small",
                "calculator": "pad_small",
                "org.qutebrowser.qutebrowser": "pad_large",
                "rnote": "pad_extra_large",
                "discord": "pad_tall",
                "mpv": "pad_wide",
                "mpv-float": "pad_wide",
                "feh": "pad_large",
                "firefox": "pad_large",
                "Alacritty": "pad_large",
                "foot": "pad_large",
                "thunar": "pad_large",
                "gimp": "pad_extra_large",
                "obsidian": "pad_extra_large",
                "kitty": "pad_large",
            },
            "container_select_mode.border_color": colors["orange"],
            "container_select_mode.border_size": BORDER_WIDTH,
            "tab_bar.height": BORDER_WIDTH * 2,
            "tab_bar.margin": [0, GAP, 0, GAP],
            "tab_bar.bg_color": colors["bg0"],
            "tab_bar.tab.font_size": 1,
            "L1.tab_bar.hide_when": "always",
            "L2.tab_bar.tab.bg_color": colors["cyan_dimmed"],
            "L2.tab_bar.tab.active.bg_color": colors["cyan"],
            "L3.tab_bar.tab.bg_color": colors["purple_dimmed"],
            "L3.tab_bar.tab.active.bg_color": colors["purple"],
            "L4.tab_bar.tab.bg_color": colors["blue_dimmed"],
            "L4.tab_bar.tab.active.bg_color": colors["blue"],
            "L5.tab_bar.tab.bg_color": colors["yellow_dimmed"],
            "L5.tab_bar.tab.active.bg_color": colors["yellow"],
            "L6.tab_bar.tab.bg_color": colors["green_dimmed"],
            "L6.tab_bar.tab.active.bg_color": colors["green"],
            "L7.tab_bar.tab.bg_color": colors["red_dimmed"],
            "L7.tab_bar.tab.active.bg_color": colors["red"],
        }
    ),
]

floating_layout = layout.Floating(
    border_width=BORDER_WIDTH,
    border_focus=BORDER_COLOR,
    border_normal=colors["bg0"],
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="branchdialog"),
        Match(title="pinentry"),
        Match(wm_class="kitty-float"),
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="vimiv"),
        Match(wm_class="mpv-float"),
        Match(wm_class="mpv"),
        Match(wm_class="matplotlib"),
        Match(wm_class="feh"),
        Match(wm_class="fileselect"),
        Match(wm_class="discord"),
        Match(wm_class="steam"),
        Match(wm_class="steamwebhelper"),
    ],
)
