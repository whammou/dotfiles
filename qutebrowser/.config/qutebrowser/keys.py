# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103


# KEYBINNDINGS
# Bindings for normal mode
config.unbind("d")
config.unbind("D")
config.unbind("F")
# config.unbind("j")
# config.unbind("k")

# Input method
# config.bind("<Escape>", "spawn fcitx5-remote -s keyboard-us", mode="insert")
# ~/.config/qutebrowser/config.py


# Bind Escape in insert mode to switch Fcitx5 and then leave insert mode
# This might require two presses or careful timing, as qutebrowser's own
# Escape handling might still fire.config.bind('o', 'set statusbar.show always;; set-cmd-text -s :open')
config.bind("<Control-e>", "scroll-px 0 34")
config.bind("<Control-y>", "scroll-px 0 -34")
config.bind(
    "<Escape>", "mode-enter normal;; set statusbar.show in-mode", mode="command"
)
config.bind("<Return>", "command-accept;; set statusbar.show in-mode", mode="command")

config.bind(
    "<Escape>",
    "spawn fcitx5-remote -s keyboard-us ;; mode-leave",
    mode="insert",
)

config.bind("i", "set statusbar.show in-mode ;; mode-enter insert", mode="normal")
config.bind(
    "<Control-i>",
    "set statusbar.show in-mode ;; spawn fcitx5-remote -s unikey ;; mode-enter insert",
    mode="normal",
)
config.bind("/", "cmd-set-text -s :search ;; set statusbar.show always", mode="normal")
config.bind(
    "?", "cmd-set-text -s :search -r;; set statusbar.show always", mode="normal"
)

# Settings
config.bind("xb", "set statusbar.show never")
config.bind(
    "xc",
    "config-cycle content.user_stylesheets ~/.config/qutebrowser/css/default.css ~/.config/qutebrowser/css/custom-onedark.css",
)
config.bind("xd", "config-cycle colors.webpage.darkmode.enabled True False")
config.bind("xt", "config-cycle tabs.show multiple always")
# Qtile
c.aliases["split"] = "spawn _qtile_spawn_split_y"
c.aliases["vsplit"] = "spawn _qtile_spawn_split_x"
c.aliases["tab"] = "spawn _qtile_spawn_tab"
c.aliases["tab_new"] = "spawn _qtile_spawn_new_tab"
c.aliases["screen"] = "spawn _qtile_spawn_screen"

config.bind("o", "set statusbar.show always ;; cmd-set-text -s :open")
config.bind("O", "set statusbar.show always ;; cmd-set-text -s :open -t")
config.bind("X", "set statusbar.show always ;; cmd-set-text -s :split")
config.bind("V", "set statusbar.show always ;; cmd-set-text -s :vsplit", mode="normal")
config.bind("T", "set statusbar.show always ;; cmd-set-text -s :tab")
config.bind("<Ctrl-T>", "set statusbar.show always ;; cmd-set-text -s :tab_new")

config.bind("f", "set statusbar.show never ;; hint all")
config.bind("FI", "set statusbar.show never ;; hint images spawn xdg-open {hint-url}")
config.bind("Fi", "set statusbar.show never ;; hint inputs")
config.bind(
    "Fv",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_split -a 'xdg-open {hint-url}' x",
)
config.bind(
    "Fx",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_split -a 'xdg-open {hint-url}' y",
)
config.bind(
    "Ft",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o layout -f spawn_tab -a 'xdg-open {hint-url}'",
)
config.bind(
    "FT",
    "set statusbar.show never ;; hint all spawn _qtile_spawn_new_tab '{hint-url}'",
)
config.bind(
    "Ff",
    "set statusbar.show never ;; hint all spawn qtile cmd-obj -o root -f spawn -a 'xdg-open {hint-url}'",
)
config.bind(
    "FF",
    "set statusbar.show never ;; hint all tab-bg",
)
config.bind(";a", "set statusbar.show never ;; hint all yank")
# Medias
config.bind(
    "M",
    "set statusbar.show never ;; hint all spawn mpv --x11-name='mpv-float' {hint-url}",
)
# Navigation
config.bind("m", "mode-enter set_mark ;; message-info 'Set Scroll Mark:'")
