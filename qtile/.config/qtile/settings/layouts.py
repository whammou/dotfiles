from libqtile import hook, layout, qtile
from libqtile.config import Match
from qtile_bonsai import Bonsai

from .screens import GAP, OFFSET
from .theme import colors
from .smart_bonsai import smart_split
import os

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


def restore_tree_view(group):
    """Restore Bonsai's tree view to show the last tiled window's tab."""
    if group.layout.last_focused_window:
        group.layout.focus(group.layout.last_focused_window)
        group.layout_all()


def restore_focus(window):
    """Restore focus to window and re-enable floating hide."""
    global _suppress_floating_hide
    _suppress_floating_hide = False
    if window.group is not None:
        window.group.focus(window)


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


# @hook.subscribe.group_window_add
# def maintain_focus(group, window):
#    history = group.focus_history
#    prev_floating = history[-1]
#    prev_window = history[-2]
#
#    if group.current_window.floating and len(history) > 1:
#        group.qtile.call_soon(lambda: group.focus(prev_window))
#    group.qtile.call_soon(lambda: group.focus(prev_floating))


class MyCustomBonsai(Bonsai):
    def __init__(self, *args, **kwargs):
        self.excluded_wm_classes = kwargs.pop("excluded_wm_classes", [])
        super().__init__(*args, **kwargs)
        self.last_focused_window = None

    def focus(self, window):
        if self.focused_window:
            self.last_focused_window = self.focused_window
        super().focus(window)

    def _handle_add_client__normal(self, window):
        wm_class = window.get_wm_class()
        if wm_class and self._is_excluded(wm_class):
            pane = self._tree.tab()
            self._reset_next_window_handler()
            return pane
        return super()._handle_add_client__normal(window)

    def _is_excluded(self, wm_class):
        """Check if a window's WM_CLASS matches any excluded class (case-insensitive)."""
        if not self.excluded_wm_classes:
            return False
        wm_lower = [c.lower() for c in wm_class]
        return any(exc.lower() in wm_lower for exc in self.excluded_wm_classes)


@hook.subscribe.group_window_add
def maintain_focus(group, window):
    global _suppress_floating_hide

    prev_window = group.current_window
    if prev_window is not None:
        if prev_window.floating:
            _suppress_floating_hide = True
            # Deferred: Qtile's auto-focus of the new window will
            # update the tree view to B's tab via Bonsai.focus(new).
            # Run AFTER that to restore view to the last tiled tab.
            group.qtile.call_soon(lambda: restore_tree_view(group))
        group.qtile.call_soon(lambda: restore_focus(prev_window))


@hook.subscribe.client_killed
def after_kill_fallback(window):
    group = window.group
    if group and len(group.focus_history) > 1:
        current_window = group.focus_history[-2]

        group.qtile.call_soon(lambda: group.focus(group.layout.last_focused_window))
        if current_window.floating:
            group.qtile.call_soon(lambda: group.focus(current_window))


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
            "excluded_wm_classes": ["mpv"],
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
        Match(wm_class="matplotlib"),
        Match(wm_class="feh"),
        Match(wm_class="fileselect"),
        Match(wm_class="discord"),
        Match(wm_class="steam"),
        Match(wm_class="steamwebhelper"),
    ],
)
