# Entry point for layout configuration.
#
# Helpers live in .layout.commands, hook subscriptions in .layout.hooks.
# Importing them here registers the hooks; the re-exports below keep
# `from settings.layouts import ...` working for existing callers.

from libqtile import layout
from libqtile.config import Match, MatchAny, _Match

import re
from dataclasses import dataclass

from .layout.custom_bonsai import SmartBonsai
from .screens import GAP
from .theme import colors
from .smart_bonsai import smart_split, smart_split_optimal

from .layout import hooks  # noqa: F401  (side-effect: hook registration)

from .layout.commands import (  # noqa: F401  (backward-compat re-exports)
    _forget,
    _remember_toggle_geom,
    _restore_toggle_geom,
    hide_floating_win,
    is_floating_hidden,
    show_floating_win,
    toggle_floating_minimize,
)

# Window rules (canonical definitions — edit here).
# One list drives floating (float_rules below), floating size (``size`` preset,
# applied by the client_managed hook) and focus-steal (_is_focus_allowed in
# .layout.commands). Absence from this list means tile + no steal (e.g.
# StartCenter). Patterns are case-insensitive; extend with values from
# `qtile cmd-obj -o window -f info`.
# Rules with ``floating=False`` still carry a ``size`` so spawn_float can size
# apps that normally tile (nvim, yazi, org-*, ...); the hook ignores them.


def _re(pat: str) -> re.Pattern:
    return re.compile(pat, re.IGNORECASE)


def _either(token: str) -> MatchAny:
    """Match token anywhere in window title OR any wm_class entry."""
    return MatchAny(Match(title=_re(".*" + token)), Match(wm_class=_re(".*" + token)))


def _cls(*names: str) -> Match:
    """Exact, case-insensitive WM_CLASS entry match (instance or class).

    Unlike ``_re``, ``yazi`` will not also match ``yazi-journal``, so each class
    can carry its own preset.
    """
    return Match(
        wm_class=re.compile(
            r"^(" + "|".join(map(re.escape, names)) + r")$", re.IGNORECASE
        )
    )


@dataclass(frozen=True)
class WinRule:
    """Match a window to float, size and/or focus-steal actions.

    ``size`` is a scratchpad preset name (see ``settings/group/scratchpads.py``)
    or an explicit ``(width, height)`` pair, applied once this rule has floated
    the window. ``None`` keeps the app's own geometry, which is what the generic
    ``wm_type`` catch-alls rely on so dialogs are not resized. Entries with
    ``floating=False`` still carry a ``size`` for ``spawn_float``.
    """

    match: _Match
    floating: bool = False
    focus: bool = False
    focus_match: _Match | None = None
    size: str | tuple[int, int] | None = None


WIN_RULES = (
    # Float + focus + preset.
    WinRule(
        _cls(
            "bluetuith",
            "calculator",
            "chessterm",
            "fzf-emoji",
            "kari",
            "xset",
            "yt-x",
        ),
        floating=True,
        focus=True,
        size="pad_small",
    ),
    WinRule(
        _cls(
            "btm",
            "ncdu",
            "notification-history",
            "nvtop",
            "sysz",
        ),
        floating=True,
        focus=True,
        size="pad_medium",
    ),
    WinRule(
        _cls("mon-battery", "voltage", "watch-cpu"),
        floating=True,
        focus=True,
        size="pad_list",
    ),
    WinRule(
        _cls("typing"),
        floating=True,
        focus=True,
        size="pad_typing",
    ),
    # Float + focus, app sizes itself.
    WinRule(
        MatchAny(
            _cls("fileselect", "network", "ssh-askpass"),
            Match(title=_re("^branchdialog")),
            Match(title=_re("^pinentry")),
            Match(wm_class=_re("xdg-desktop-portal")),
        ),
        floating=True,
        focus=True,
    ),
    WinRule(
        _cls("qutebrowser-editor"),
        floating=True,
        focus=True,
        focus_match=_either("qutebrowser-editor"),
    ),
    WinRule(
        _cls("dict"),
        floating=True,
        focus=True,
        focus_match=_either("dict"),
        size="pad_small",
    ),
    WinRule(
        Match(
            wm_class=_re("(soffice|libreoffice|libreoffice-startcenter)"),
            title=_re(
                r"^(Select\b|open\b|save\b|insert\b|print\b|confirm\b|hyperlink\b|export\b|find\b|Error\b|"
                r"spelling\b|character\b|paragraph\b|delete\b|warning\b|thesaurus\b|"
                r"word count\b|page style\b|bullets\b|special characters\b|"
                r"track changes\b|comments\b|mail merge\b|navigator\b|properties\b)"
            ),
        ),
        floating=True,
        focus=True,
    ),
    # Focus only, stay tiled.
    WinRule(
        MatchAny(
            Match(title=_re(r".*libreoffice (writer|calc)$")),
            Match(title=_re("volume control")),
        ),
        focus=True,
    ),
    # Float only, with preset.
    WinRule(
        _cls("mpv", "mpv-float"),
        floating=True,
    ),
    WinRule(
        _cls("feh"),
        floating=True,
        size="pad_large",
    ),
    WinRule(
        _cls("discord"),
        floating=True,
        size="pad_tall",
    ),
    # Float only, no preset.
    WinRule(
        MatchAny(
            _cls(
                "confirmreset",
                "kitty-float",
                "makebranch",
                "maketag",
                "matplotlib",
                "org.pulseaudio.pavucontrol",
                "steam",
                "steamwebhelper",
                "vimiv",
            ),
            Match(wm_type="dialog"),
            Match(wm_type="utility"),
        ),
        floating=True,
    ),
    # Spawn-only presets: these apps tile normally, so floating stays False and
    # only spawn_float consumes the size. The hook skips them, which is what
    # keeps a Firefox save dialog from being stretched to pad_large.
    WinRule(
        _cls(
            "alacritty",
            "firefox",
            "foot",
            "kitty",
            "lazygit-dotfiles",
            "lazygit-journal",
            "neomutt",
            "newsboat",
            "nvim",
            "org-agenda",
            "org-backlog",
            "org-browse",
            "org-search",
            "org-super-agenda",
            "org.qutebrowser.qutebrowser",
            "ssh-session",
            "sys-upgrade",
            "thunar",
            "tmux-session",
            "yazi-journal",
        ),
        size="pad_large",
    ),
    WinRule(
        _cls("yazi", "yazi-sftp"),
        size="pad_medium",
    ),
    WinRule(
        _cls(
            "ani-cli",
            "anifzf",
            "mangal",
            "notif-history",
            "opencode",
            "opencode-attach",
            "org-capture",
            "org-roam-capture",
        ),
        size="pad_small",
    ),
    WinRule(
        _cls("gimp", "obsidian", "rnote", "test-session"),
        size="pad_extra_large",
    ),
    WinRule(
        _cls("mon-voltage", "tlp-recalibrate"),
        size="pad_list",
    ),
)

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
            "window.default_add_mode": smart_split_optimal,
            "excluded_wm_classes": [],
            "container_select_mode.border_color": colors["green"],
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
        *(rule.match for rule in WIN_RULES if rule.floating),
    ],
)
