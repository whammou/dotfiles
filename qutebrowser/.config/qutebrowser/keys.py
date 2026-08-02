import os
from typing import Any

from paths import CSS_DIR

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# pylint: disable=C0111


# KEYBINNDINGS
# Bindings for normal mode
config.unbind("d")
config.unbind("D")
config.unbind("F")
config.unbind("<Control-e>", mode="insert")
# config.unbind("j")
# config.unbind("k")

config.bind(
    "xp",
    "config-cycle --temp content.proxy socks5://127.0.0.1:1080 system ;; message-info 'Toggled proxy'",  # noqa: E501
)
# Input method
# config.bind("<Escape>", "spawn fcitx5-remote -s keyboard-us", mode="insert")
# ~/.config/qutebrowser/config.py
config.bind(
    "<Control-e>",
    "edit-text ;; message-info 'Opened in Editor'",
    mode="insert",
)
config.bind(
    "<Escape>",
    "spawn fcitx5-remote -s keyboard-us ;; mode-leave",
    mode="insert",
)
config.bind(
    "<Escape>",
    "spawn fcitx5-remote -s keyboard-us",
    mode="normal",
)
config.bind(
    "<Control-i>",
    "set statusbar.show in-mode ;; spawn fcitx5-remote -s unikey",
    mode="insert",
)

# Bind Escape in insert mode to switch Fcitx5 and then leave insert mode
# This might require two presses or careful timing, as qutebrowser's own
# Escape handling might still fire.config.bind('o', 'set statusbar.show always;; set-cmd-text -s :open')  # noqa: E501
config.bind("<Control-e>", "scroll-px 0 34")
config.bind("<Control-y>", "scroll-px 0 -34")
config.bind(
    "<Escape>", "mode-enter normal;; set statusbar.show in-mode", mode="command"  # noqa: E501
)
config.bind("<Return>", "command-accept;; set statusbar.show in-mode", mode="command")  # noqa: E501
config.bind("i", "set statusbar.show in-mode ;; mode-enter insert", mode="normal")  # noqa: E501
config.bind("/", "cmd-set-text -s :search ;; set statusbar.show always", mode="normal")  # noqa: E501
config.bind(
    "?", "cmd-set-text -s :search -r;; set statusbar.show always", mode="normal"  # noqa: E501
)

# Settings
config.bind("xb", "set statusbar.show never")
config.bind("<Ctrl-r>", "toggle-tab-css")
config.bind(
    "xc",
    "config-cycle --temp content.user_stylesheets "
    "'[" + os.path.expanduser(CSS_DIR) + "default.css]' "
    "'[" + ", ".join(c.content.user_stylesheets) + "]'",
)
config.bind("xd", "config-cycle --temp colors.webpage.darkmode.enabled True False")  # noqa: E501
config.bind("xt", "config-cycle --temp tabs.show multiple always")
# Qtile
c.aliases["split"] = "spawn _qtile_spawn_split_y"
c.aliases["vsplit"] = "spawn _qtile_spawn_split_x"
c.aliases["tab"] = "spawn _qtile_spawn_tab"
c.aliases["tab_new"] = "spawn _qtile_spawn_new_tab"
c.aliases["screen"] = "spawn _qtile_spawn_screen"

config.bind("o", "set statusbar.show always ;; cmd-set-text -s :open")
config.bind("O", "set statusbar.show always ;; cmd-set-text -s :open -t")
config.bind("<Ctrl+o>", "set statusbar.show always ;; cmd-set-text -s :screen")
config.bind("X", "set statusbar.show always ;; cmd-set-text -s :split")
config.bind("V", "set statusbar.show always ;; cmd-set-text -s :vsplit", mode="normal")  # noqa: E501
config.bind("T", "set statusbar.show always ;; cmd-set-text -s :tab")
config.bind("<Ctrl-T>", "set statusbar.show always ;; cmd-set-text -s :tab_new")  # noqa: E501

config.bind("f", "set statusbar.show never ;; hint all")
config.bind("FO", "set statusbar.show never ;; hint all tab")
config.bind("FI", "set statusbar.show never ;; hint images spawn xdg-open {hint-url}")  # noqa: E501
config.bind("Fi", "set statusbar.show never ;; hint inputs")
config.bind(
    "Fv",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_split -a 'xdg-open {hint-url}' x",  # noqa: E501
)
config.bind(
    "Fx",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_split -a 'xdg-open {hint-url}' y",  # noqa: E501
)
config.bind(
    "Ft",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_tab -a 'xdg-open {hint-url}'",  # noqa: E501
)
config.bind(
    "FT",
    "set statusbar.show never ;; hint all spawn _qtile_spawn_new_tab '{hint-url}'",  # noqa: E501
)
config.bind(
    "FF",
    # "set statusbar.show never ;; hint all spawn qtile cmd-obj -o root -f spawn -a 'xdg-open {hint-url}'",  # noqa: E501
    "set statusbar.show never ;; hint all spawn _qtile_spawn_screen '{hint-url}'",  # noqa: E501
)
config.bind(
    "Ff",
    "set statusbar.show never ;; hint all spawn xdg-open {hint-url}",
)
config.bind(";a", "set statusbar.show never ;; hint all yank")
# Medias
config.bind(
    "M",
    "set statusbar.show never ;; hint all spawn mpv --x11-name='mpv-float' {hint-url}",  # noqa: E501
)
# Navigation
config.bind("m", "mode-enter set_mark ;; message-info 'Set Scroll Mark:'")
