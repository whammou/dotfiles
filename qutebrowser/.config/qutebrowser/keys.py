import os
import subprocess
from typing import Any

from lib.paths import CSS_DIR
from qutebrowser.api import cmdutils
from qutebrowser.completion.models import urlmodel

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# pylint: disable=C0111


def bind_modes(key: str, command: str, modes: list[str]) -> None:
    """Bind a key to the same command in several modes."""
    for mode in modes:
        config.bind(key, command, mode=mode)


# unbind: {{{
config.unbind("d")
config.unbind("D")
config.unbind("F")
config.unbind("<Control-e>", mode="insert")
# config.unbind("j")
# config.unbind("k")
# }}}

# proxy: {{{
config.bind(
    "xp",
    "config-cycle --temp content.proxy socks5://127.0.0.1:1080 system ;; message-info 'Toggled proxy'",  # noqa: E501
)
# }}}

# input method (fcitx5): {{{
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
bind_modes(
    "<Control-i>",
    "set statusbar.show in-mode ;; spawn fcitx5-remote -s unikey",
    ["insert", "command"],
)
# }}}

# scrolling: {{{
config.bind("<Control-e>", "scroll-px 0 34")
config.bind("<Control-y>", "scroll-px 0 -34")
# }}}

# statusbar/mode binds: {{{
# Bind Escape in insert mode to switch Fcitx5 and then leave insert mode
# This might require two presses or careful timing, as qutebrowser's own
# Escape handling might still fire.config.bind('o', 'set statusbar.show always;; set-cmd-text -s :open')  # noqa: E501
config.bind(
    "<Escape>", "mode-enter normal;; set statusbar.show in-mode", mode="command"  # noqa: E501
)
config.bind("<Return>", "command-accept;; set statusbar.show in-mode", mode="command")  # noqa: E501
config.bind("i", "set statusbar.show in-mode ;; mode-enter insert", mode="normal")  # noqa: E501
config.bind("/", "cmd-set-text -s :search ;; set statusbar.show always", mode="normal")  # noqa: E501
config.bind(
    "?", "cmd-set-text -s :search -r;; set statusbar.show always", mode="normal"  # noqa: E501
)
# }}}

# settings toggles: {{{
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
# }}}

# qtile commands: {{{
# Registered commands (not aliases) so the completer offers the same URL
# suggestions as :open; aliases are invisible to the completion system.
def _qtile_spawn(exe: str, url: str | None) -> None:
    subprocess.Popen([exe] + ([url] if url else []))


try:
    @cmdutils.register(name="split", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split(url=None) -> None:
        """Open URL in a new qtile split window."""
        _qtile_spawn("_qtile_spawn_split_y", url)

    @cmdutils.register(name="vsplit", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def vsplit(url=None) -> None:
        """Open URL in a new qtile vertical split window."""
        _qtile_spawn("_qtile_spawn_split_x", url)

    @cmdutils.register(name="tab", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab(url=None) -> None:
        """Open URL in a new qtile tab."""
        _qtile_spawn("_qtile_spawn_tab", url)

    @cmdutils.register(name="tab_new", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab_new(url=None) -> None:
        """Open URL in a new qtile window."""
        _qtile_spawn("_qtile_spawn_new_tab", url)

    @cmdutils.register(name="screen", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def screen(url=None) -> None:
        """Open URL on a new qtile screen."""
        _qtile_spawn("_qtile_spawn_screen", url)
except ValueError:
    # Re-sourcing keys.py (e.g. :config-source) would re-register commands
    # that already exist; keep the existing registrations.
    pass
# }}}

# open/cmd binds: {{{
config.bind("o", "set statusbar.show always ;; cmd-set-text -s :open")
config.bind("O", "set statusbar.show always ;; cmd-set-text -s :open -t")
config.bind("<Ctrl+o>", "set statusbar.show always ;; cmd-set-text -s :screen")
config.bind("X", "set statusbar.show always ;; cmd-set-text -s :split")
config.bind("V", "set statusbar.show always ;; cmd-set-text -s :vsplit", mode="normal")  # noqa: E501
config.bind("T", "set statusbar.show always ;; cmd-set-text -s :tab")
config.bind("<Ctrl-T>", "set statusbar.show always ;; cmd-set-text -s :tab_new")  # noqa: E501
# }}}

# hint binds: {{{
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
# }}}

# media: {{{
config.bind(
    "M",
    "set statusbar.show never ;; hint all spawn mpv --x11-name='mpv-float' {hint-url}",  # noqa: E501
)
# }}}

# navigation: {{{
config.bind("m", "mode-enter set_mark ;; message-info 'Set Scroll Mark:'")
# }}}
# vim: foldmethod=marker foldlevel=0
