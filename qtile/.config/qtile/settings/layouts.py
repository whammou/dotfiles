from libqtile import hook, layout, qtile
from libqtile.command.base import expose_command
from libqtile.config import Match
from qtile_bonsai import Bonsai

from .screens import GAP, OFFSET
from .theme import colors
from .smart_bonsai import smart_split
from .group.scratchpads import scratchpad_layout
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
    """Restore focus to window. The suppression flag is reset by on_client_focus."""
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
    _suppress_floating_hide = False


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
        self.float_sizes = kwargs.pop("float_sizes", {})
        super().__init__(*args, **kwargs)
        self.last_focused_window = None
        self._pending_float = False

    def _spawn_program(self, program: str):
        """
        Override: clear any stale ``_pending_float`` before spawning.

        ``_spawn_program`` is the single gateway for all layout-initiated
        spawns (``spawn_split``, ``spawn_tab``, ``spawn``).  By clearing
        the flag here we cover every non-float spawn path automatically,
        including any future methods the parent class might add.
        """
        self._pending_float = False
        super()._spawn_program(program)

    @expose_command
    def spawn_float(self, program: str):
        """
        Launch the provided program and ensure the resulting window is floating.

        Like ``spawn_split`` / ``spawn_tab``, but the spawned window is placed
        on the floating layer instead of being added to the Bonsai tree.
        """
        self._pending_float = True
        # Bypass _spawn_program (which would clear _pending_float) by calling
        # the parent implementation directly.
        Bonsai._spawn_program(self, program)

    @expose_command
    def spawn(self, program: str):
        """
        Plain spawn — clears ``_pending_float``, then delegates.

        Replacement for ``lazy.spawn()`` in keybindings that need the flag
        cleared (e.g. ``mod+s`` which otherwise leaves a stale float flag
        after a cancelled ``spawn_float``).
        """
        self._spawn_program(program)

    def add_client(self, window):
        if self._pending_float:
            self._pending_float = False
            self._reset_next_window_handler()
            window.enable_floating()
            if window.group:
                window.group.mark_floating(window, True)
                self._apply_float_size(window)
            return
        super().add_client(window)

    def _apply_float_size(self, window):
        """Apply configured size preset to a floating window."""
        wm_class = window.get_wm_class()
        if not wm_class:
            return
        klass = wm_class[0].lower()
        spec = self.float_sizes.get(klass)
        if not spec:
            return
        screen = window.group.screen
        if not screen:
            return

        if isinstance(spec, str):
            geom = scratchpad_layout(preset=spec)
            sw, sh = screen.width, screen.height
            w = int(sw * geom["width"])
            h = int(sh * geom["height"])
        else:
            w, h = int(spec[0]), int(spec[1])

        window.set_size_floating(w, h)
        window.center()

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
        # Keep focus on the current window when a new window spawns,
        # regardless of window type (float or tiled). Without this,
        # new windows steal focus on creation.
        group.qtile.call_soon(lambda: restore_focus(prev_window))


@hook.subscribe.client_killed
def after_kill_fallback(window):
    group = window.group
    if not group:
        return

    # When a floating window is killed (e.g. LibreOffice transient banner),
    # don't run the floating-window-priority focus path — let qtile's
    # default focus handling (focus_previous_on_window_remove) take over.
    if window.floating:
        return

    def restore():
        # Qtile's built-in focus handling (focus_previous_on_window_remove
        # and layout.remove()) already resolved focus. Don't override it.
        if group.current_window is not window:
            return

        # Genuine fallback: no window was focused by qtile's defaults.
        # Restore the layout's last focused window, but only if it's
        # tiling — focusing a floating window here would trigger a
        # show/hide cascade that creates a flicker.
        target = group.layout.last_focused_window
        if target and not target.floating:
            group.focus(target)

    group.qtile.call_soon(restore)


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
        Match(wm_class="matplotlib"),
        Match(wm_class="feh"),
        Match(wm_class="fileselect"),
        Match(wm_class="discord"),
        Match(wm_class="steam"),
        Match(wm_class="steamwebhelper"),
    ],
)
