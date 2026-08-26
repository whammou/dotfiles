from libqtile import hook, layout, qtile
from libqtile.config import Match
import os

from .layout.custom_bonsai import MyCustomBonsai
from .screens import GAP, OFFSET
from .theme import colors
from .smart_bonsai import smart_split

_last_focused = None
_suppress_floating_hide = False
_floating_sound_startup = True


def hide_floating_win(window):
    """Hide a floating window off-screen."""
    if window.floating and not window.fullscreen:
        window.set_position_floating(-9999, -9999)


def show_floating_win(window):
    """Show a floating window centered and at front."""
    if window.floating and not window.fullscreen:
        window.bring_to_front()
        window.center()


@hook.subscribe.client_managed
def hide_floating(window):
    hide_floating_win(window)


@hook.subscribe.startup_complete
def _disable_floating_sound_startup():
    """Disable the startup guard after Qtile finishes initializing."""
    global _floating_sound_startup
    _floating_sound_startup = False


@hook.subscribe.client_managed
def play_floating_sound(window):
    """Play a notification sound when a floating window appears."""
    global _floating_sound_startup
    if _floating_sound_startup:
        return
    if window.floating:
        sound_path = os.path.expanduser("~/.local/share/bell/staplebops-05.wav")
        qtile.spawn(f"pw-play --media-role=Notification --volume=1.0 {sound_path}")


@hook.subscribe.client_focus
def on_client_focus(window):
    global _last_focused, _suppress_floating_hide

    if (
        _last_focused is not None
        and _last_focused.floating
        and not _suppress_floating_hide
    ):
        try:
            hide_floating_win(_last_focused)
        except (AttributeError, RuntimeError):
            pass

    show_floating_win(window)
    _last_focused = window
    _suppress_floating_hide = False



@hook.subscribe.group_window_add
def no_focus_steal(group, window):
    prev = group.current_window
    if prev is not None:
        window.can_steal_focus = False
        qtile_inst = getattr(group, "qtile", None)
        if qtile_inst:

            def _reclaim():
                if getattr(window, "floating", False) and window.group is group and prev.group is group:
                    group.focus(prev, warp=False)

            qtile_inst.call_soon(_reclaim)


@hook.subscribe.group_window_remove
def after_killed_focus_same_L1(group, window):
    from qtile_bonsai import Bonsai
    from qtile_bonsai.core.nodes import Tab

    layout = group.layout
    if not isinstance(layout, Bonsai):
        return
    if layout._tree.is_empty:
        return
    try:
        qtile_inst = getattr(group, "qtile", None)
        is_floating = bool(getattr(window, "floating", False))
        # capture killed window's L1 tab before Group removes it — stay in same L1, no tab switch
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
                if target and not target.floating and target.group is group:
                    if group.current_window is not target:
                        group.focus(target, warp=False)
            except Exception:
                return

        if qtile_inst:
            qtile_inst.call_soon(_restore)
        _restore()
    except Exception:
        return


BORDER_WIDTH = 3
BORDER_COLOR = colors["grey"]

layouts = [
    MyCustomBonsai(
        **{
            "auto_cwd_for_terminals": False,
            "window.border_size": BORDER_WIDTH,
            "window.single.border_size": BORDER_WIDTH,
            "window.border_color": colors["bg0"],
            "window.active.border_color": BORDER_COLOR,
            "window.margin": [0, GAP, GAP * 2, GAP],
            "window.default_add_mode": smart_split,
            "excluded_wm_classes": [
                # "mpv"
            ],
            "float_sizes": {
                # -- kitty --app-id terminal apps
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
                # Native / GUI apps (set their own app_id)
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
                # Fallback generic kitty (no --app-id)
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
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="kitty-float"),  # gitk
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
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
