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


# unbind: {{{
config.unbind("d")
config.unbind("D")
config.unbind("F")
config.unbind("<Control-e>", mode="insert")
# dropped shorts: defaults (e.g. O -> :open -t) resurface once custom binds are removed
config.unbind("O")
config.unbind("X")
config.unbind("V")
config.unbind("T")
config.unbind("<Ctrl-T>")
config.unbind("<Ctrl+o>")
# config.unbind("j")
# config.unbind("k")
# }}}

# proxy: {{{
# Toggle SOCKS5 proxy (127.0.0.1:1080) on/off
config.bind(
    "xp",
    "config-cycle --temp content.proxy socks5://127.0.0.1:1080 system ;; message-info 'Toggled proxy'",  # noqa: E501
)
# }}}

# input method (fcitx5): {{{
# Edit text in external editor (insert/command mode)
config.bind(
    "<Control-e>",
    "edit-text ;; message-info 'Opened in Editor'",
    mode="insert",
)
# Switch fcitx5 to US keyboard and leave insert mode
config.bind(
    "<Escape>",
    "spawn fcitx5-remote -s keyboard-us ;; mode-leave",
    mode="insert",
)
# Switch fcitx5 to US keyboard + default Escape (clear keychain/search/fullscreen)
config.bind(
    "<Escape>",
    "spawn fcitx5-remote -s keyboard-us ;; clear-keychain ;; search ;; fullscreen --leave",  # noqa: E501
    mode="normal",
)
# }}}

# scrolling: {{{
# Scroll down 34px
config.bind("<Control-e>", "scroll-px 0 34")
# Scroll up 34px
config.bind("<Control-y>", "scroll-px 0 -34")
# }}}

# statusbar/mode binds: {{{
# Leave command mode (default), restore statusbar
config.bind(
    "<Escape>",
    "mode-leave ;; set statusbar.show in-mode",
    mode="command",  # noqa: E501
)
# Accept command input, restore statusbar
config.bind("<Return>", "command-accept;; set statusbar.show in-mode", mode="command")  # noqa: E501
# Enter insert mode, show statusbar
config.bind("i", "set statusbar.show in-mode ;; mode-enter insert", mode="normal")  # noqa: E501
# Forward search prompt
config.bind("/", "cmd-set-text -s :search ;; set statusbar.show always", mode="normal")  # noqa: E501
# Reverse search prompt
config.bind(
    "?",
    "cmd-set-text -s :search -r;; set statusbar.show always",
    mode="normal",  # noqa: E501
)
# }}}

# settings toggles: {{{
# Hide statusbar
config.bind("xb", "set statusbar.show never")
# Toggle custom tab CSS
config.bind("<Ctrl-r>", "toggle-tab-css")
# Toggle custom user stylesheets
config.bind(
    "xc",
    "config-cycle --temp content.user_stylesheets "
    "'[" + os.path.expanduser(CSS_DIR) + "default.css]' "
    "'[" + ", ".join(c.content.user_stylesheets) + "]'",
)
# Toggle dark mode
config.bind("xd", "config-cycle --temp colors.webpage.darkmode.enabled True False")  # noqa: E501
# Toggle tab bar visibility
config.bind("xt", "config-cycle --temp tabs.show multiple always")
# }}}

# qtile commands: {{{
# Registered commands (not aliases) so the completer offers the same URL
# suggestions as :open; aliases are invisible to the completion system.


def _qtlcmd(func: str, url: str | None, *extra: str) -> None:
    prog = f"qb '{url}'" if url else "qb"
    subprocess.Popen(["qtlcmd", "-o", "layout", "-f", func, "-a", prog, *extra])


try:

    @cmdutils.register(name="split", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split(url=None) -> None:
        """Open URL in a new qtile split window."""
        _qtlcmd("spawn_split", url, "-a", "y")

    @cmdutils.register(name="vsplit", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def vsplit(url=None) -> None:
        """Open URL in a new qtile vertical split window."""
        _qtlcmd("spawn_split", url, "-a", "x")

    @cmdutils.register(name="tab", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab(url=None) -> None:
        """Open URL in a new qtile tab."""
        _qtlcmd("spawn_tab", url)

    @cmdutils.register(name="tab_new", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab_new(url=None) -> None:
        """Open URL in a new qtile window."""
        _qtlcmd("spawn_tab", url, "-k", "new_level=True")

    @cmdutils.register(name="screen", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def screen(url=None) -> None:
        """Open URL on a new qtile screen."""
        _qtlcmd("spawn_tab", url, "-k", "level=1")

    @cmdutils.register(name="split_left", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split_left(url=None) -> None:
        """Open URL in a qtile split to the left."""
        _qtlcmd("spawn_split", url, "-a", "x", "-k", "position=previous")

    @cmdutils.register(name="split_down", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split_down(url=None) -> None:
        """Open URL in a qtile split below."""
        _qtlcmd("spawn_split", url, "-a", "y")

    @cmdutils.register(name="split_above", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split_above(url=None) -> None:
        """Open URL in a qtile split above."""
        _qtlcmd("spawn_split", url, "-a", "y", "-k", "position=previous")

    @cmdutils.register(name="split_right", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def split_right(url=None) -> None:
        """Open URL in a qtile split to the right."""
        _qtlcmd("spawn_split", url, "-a", "x")

    @cmdutils.register(name="float", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def float_win(url=None) -> None:
        """Open URL in a qtile floating window."""
        _qtlcmd("spawn_float", url)

    @cmdutils.register(name="tab_prev", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab_prev(url=None) -> None:
        """Open URL in the previous qtile tab slot."""
        _qtlcmd("spawn_tab", url, "-k", "position=previous")

    @cmdutils.register(name="tab_next", maxsplit=0)
    @cmdutils.argument("url", completion=urlmodel.url)
    def tab_next(url=None) -> None:
        """Open URL in the next qtile tab slot."""
        _qtlcmd("spawn_tab", url, "-k", "position=next")
except ValueError:
    # Re-sourcing keys.py (e.g. :config-source) would re-register commands
    # that already exist; keep the existing registrations.
    pass
# }}}

# open/cmd binds: {{{
# Open URL prompt
config.bind("o", "set statusbar.show always ;; cmd-set-text -s :open")
# Open URL in new tab prompt (current window)
config.bind("Os", "set statusbar.show always ;; cmd-set-text -s :open -t")
# prompt parity (O prefix mirrors the F hint scheme): {{{
# Open prompt: split to the left (tiling)
config.bind("Owh", "set statusbar.show always ;; cmd-set-text -s :split_left")
# Open prompt: split below (tiling)
config.bind("Owj", "set statusbar.show always ;; cmd-set-text -s :split_down")
# Open prompt: split above (tiling)
config.bind("Owk", "set statusbar.show always ;; cmd-set-text -s :split_above")
# Open prompt: split to the right (tiling)
config.bind("Owl", "set statusbar.show always ;; cmd-set-text -s :split_right")
# Open prompt: floating window
config.bind("Ofs", "set statusbar.show always ;; cmd-set-text -s :float")
# Open prompt: previous tab slot
config.bind("Oth", "set statusbar.show always ;; cmd-set-text -s :tab_prev")
# Open prompt: new tab level
config.bind("Otj", "set statusbar.show always ;; cmd-set-text -s :tab_new")
# Open prompt: new tab
config.bind("Otk", "set statusbar.show always ;; cmd-set-text -s :tab")
# Open prompt: next tab slot
config.bind("Otl", "set statusbar.show always ;; cmd-set-text -s :tab_next")
# Open prompt: new top-level tab (screen)
config.bind("Ots", "set statusbar.show always ;; cmd-set-text -s :screen")
# }}}
# }}}

# hint binds: {{{
# Hint all links (follow in current tab)
config.bind("f", "set statusbar.show never ;; hint all")
# Hint links, open in a new tab
config.bind("FO", "set statusbar.show never ;; hint all tab")
# Hint images, open externally
config.bind("FI", "set statusbar.show never ;; hint images spawn xdg-open {hint-url}")  # noqa: E501
# Hint text inputs
config.bind("Fi", "set statusbar.show never ;; hint inputs")
# Hint links, open externally via xdg-open
config.bind(
    "Fs",
    "set statusbar.show never ;; hint all spawn xdg-open {hint-url}",
)
# wlr-which-key parity: F{w,f,t}{key} mirrors wlr menus (w=tiling, f=float, t=tab)
# tiling (wlr w h/j/k/l -> spawn_split, cf. config.yaml:829-881): {{{
# Hint links, open in a split to the left (tiling)
config.bind(
    "Fwh",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_split -a \"xdg-open '{hint-url}'\" -a x -k position=previous",  # noqa: E501
)
# Hint links, open in a split below (tiling)
config.bind(
    "Fwj",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_split -a \"xdg-open '{hint-url}'\" -a y",  # noqa: E501
)
# Hint links, open in a split above (tiling)
config.bind(
    "Fwk",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_split -a \"xdg-open '{hint-url}'\" -a y -k position=previous",  # noqa: E501
)
# Hint links, open in a split to the right (tiling)
config.bind(
    "Fwl",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_split -a \"xdg-open '{hint-url}'\" -a x",  # noqa: E501
)
# }}}
# floating (wlr f s -> spawn_float, cf. config.yaml:198-200): {{{
# Hint links, open in a floating window
config.bind(
    "Ffs",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_float -a \"xdg-open '{hint-url}'\"",  # noqa: E501
)
# }}}
# tab (wlr t h/j/k/l/s -> spawn_tab, cf. config.yaml:685-744): {{{
# Hint links, open in the previous tab slot
config.bind(
    "Fth",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_tab -a \"xdg-open '{hint-url}'\" -k position=previous",  # noqa: E501
)
# Hint links, open in a new tab level
config.bind(
    "Ftj",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_tab -a \"xdg-open '{hint-url}'\" -k new_level=True",  # noqa: E501
)
# Hint links, open in a new tab
config.bind(
    "Ftk",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_tab -a \"xdg-open '{hint-url}'\"",  # noqa: E501
)
# Hint links, open in the next tab slot
config.bind(
    "Ftl",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_tab -a \"xdg-open '{hint-url}'\" -k position=next",  # noqa: E501
)
# Hint links, open in a new top-level tab
config.bind(
    "Fts",
    "set statusbar.show never ;; hint all spawn qtlcmd -o layout -f spawn_tab -a \"xdg-open '{hint-url}'\" -k level=1",  # noqa: E501
)
# }}}
# Hint links, yank URL to clipboard
config.bind(";a", "set statusbar.show never ;; hint all yank")
# }}}

# media: {{{
# Hint links, play with floating mpv
config.bind(
    "M",
    "set statusbar.show never ;; hint all spawn mpv --x11-name='mpv-float' {hint-url}",  # noqa: E501
)
# }}}

# navigation: {{{
# Set a scroll mark at the current position
config.bind("m", "mode-enter set_mark ;; message-info 'Set Scroll Mark:'")
# }}}
# vim: foldmethod=marker foldlevel=0
