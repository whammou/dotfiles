# Entry point for layout configuration.
#
# Helpers live in .layout.commands, hook subscriptions in .layout.hooks.
# Importing them here registers the hooks; the re-exports below keep
# `from settings.layouts import ...` working for existing callers.

from libqtile import layout
from libqtile.config import Match

import re

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

# Focus-steal allowlist (canonical definition — edit here).
# Window text is lowercased before matching, so write patterns lowercase.
# Extend with values from `qtile cmd-obj -o window -f info`.
# Plain string: name OR wm_class contains it. Tuple
# (wm_class part, name part): both must match — use for titles
# shared by many apps ("Open", "Save"). None class falls back
# to matching the title only. Either part may be a compiled
# regex (matched with search); string parts stay substrings.
STEAL_FOCUS_RULES = (
    "qutebrowser-editor",
    (
        "libreoffice",
        re.compile(
            r"^(open|save|insert|print|confirm|hyperlink|export|find|"
            r"spelling|character|paragraph|delete|warning|thesaurus|"
            r"word count|page style|bullets|special characters|"
            r"track changes|comments|mail merge|navigator|properties)"
        ),
    ),
    ("libreoffice", "libreoffice writer"),
    ("libreoffice", "libreoffice calc"),
    ("xdg-desktop-portal", re.compile(r"^(open|save|print|insert)")),
    (None, "branchdialog"),
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
        Match(wm_class="xdg-desktop-portal-gtk"),
        Match(wm_type="dialog"),
        Match(wm_type="utility"),
        Match(wm_class="qutebrowser-editor"),
        Match(wm_class="xdg-desktop-portal-gtk"),
        Match(wm_class="xdg-desktop-portal-gnome"),
        Match(
            wm_class=re.compile(r"(soffice|libreoffice)"),
            title=re.compile(
                r"^(Save|Open|Export|Print|Insert|Hyperlink|Find|Spelling|Thesaurus|Word Count|Character|Paragraph|Page Style|Bullets|Special Characters|Track Changes|Comments|Mail Merge|Navigator|Properties|Confirm|Delete|Warning)"
            ),
        ),
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
