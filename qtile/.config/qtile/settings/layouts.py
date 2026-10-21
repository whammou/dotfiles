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
# One list drives floating (float_rules below) and focus-steal
# (_is_focus_allowed in .layout.commands). Absence from this list
# means tile + no steal (e.g. StartCenter).
# Patterns are case-insensitive; extend with values from
# `qtile cmd-obj -o window -f info`.


def _re(pat: str) -> re.Pattern:
    return re.compile(pat, re.IGNORECASE)


def _either(token: str) -> MatchAny:
    """Match token anywhere in window title OR any wm_class entry."""
    return MatchAny(Match(title=_re(".*" + token)), Match(wm_class=_re(".*" + token)))


@dataclass(frozen=True)
class WinRule:
    """Match a window to float and/or focus-steal actions."""

    match: _Match
    floating: bool = False
    focus: bool = False
    focus_match: _Match | None = None


WIN_RULES = (
    # App popups: float + focus on title-or-class hit.
    WinRule(Match(wm_class="fileselect"), floating=True, focus=True),
    WinRule(
        Match(wm_class="qutebrowser-editor"),
        floating=True,
        focus=True,
        focus_match=_either("qutebrowser-editor"),
    ),
    WinRule(
        Match(wm_class="dict"), floating=True, focus=True, focus_match=_either("dict")
    ),
    WinRule(
        Match(wm_class="sysz"), floating=True, focus=True, focus_match=_either("sysz")
    ),
    WinRule(
        Match(wm_class="typing"),
        floating=True,
        focus=True,
        focus_match=_either("typing"),
    ),
    WinRule(
        Match(wm_class="notification-history"),
        floating=True,
        focus=True,
        focus_match=_either("notification-history"),
    ),
    # LibreOffice dialogs: float + focus.
    WinRule(
        Match(
            wm_class=_re("(soffice|libreoffice)"),
            title=_re(
                r"^(open\b|save\b|insert\b|print\b|confirm\b|hyperlink\b|export\b|find\b|"
                r"spelling\b|character\b|paragraph\b|delete\b|warning\b|thesaurus\b|"
                r"word count\b|page style\b|bullets\b|special characters\b|"
                r"track changes\b|comments\b|mail merge\b|navigator\b|properties\b)"
            ),
        ),
        floating=True,
        focus=True,
    ),
    # LibreOffice mains: focus, stay tiled.
    WinRule(Match(title=_re(r".*libreoffice writer$")), focus=True),
    WinRule(Match(title=_re(r".*libreoffice calc$")), focus=True),
    # Portal file pickers: float + focus.
    WinRule(
        Match(
            wm_class=_re("xdg-desktop-portal"),
        ),
        floating=True,
        focus=True,
    ),
    # WinRule(
    #     Match(
    #         wm_class=_re("xdg-desktop-portal"),
    #         title=_re(r"^(open\b|save\b|print\b|insert\b)"),
    #     ),
    #     floating=True,
    #     focus=True,
    # ),
    WinRule(Match(title=_re("^branchdialog")), floating=True, focus=True),
    WinRule(Match(title=_re("volume control")), focus=True),
    WinRule(Match(wm_class="org.pulseaudio.pavucontrol"), floating=True),
    # Auth prompts must be seen, not hidden.
    WinRule(Match(title=_re("^pinentry")), floating=True, focus=True),
    WinRule(Match(wm_class="ssh-askpass"), floating=True, focus=True),
    # Generic dialogs + legacy customs: float only.
    WinRule(Match(wm_type="dialog"), floating=True),
    WinRule(Match(wm_type="utility"), floating=True),
    *(
        WinRule(Match(wm_class=cls), floating=True)
        for cls in (
            "xdg-desktop-portal-gtk",
            "xdg-desktop-portal-gnome",
            "kitty-float",
            "confirmreset",
            "makebranch",
            "maketag",
            "vimiv",
            "mpv-float",
            "mpv",
            "matplotlib",
            "feh",
            "fileselect",
            "discord",
            "steam",
            "steamwebhelper",
        )
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
                "notification-history": "pad_medium",
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
