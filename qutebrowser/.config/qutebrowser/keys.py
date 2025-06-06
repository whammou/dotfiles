# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103


# KEYBINNDINGS
# Bindings for normal mode
config.unbind("d")
config.unbind("D")
config.unbind("F")

c.aliases["split"] = "spawn _qtile_spawn_split_y"
c.aliases["vsplit"] = "spawn _qtile_spawn_split_x"
c.aliases["tab"] = "spawn _qtile_spawn_tab"
c.aliases["tab_new"] = "spawn _qtile_spawn_new_tab"
c.aliases["screen"] = "spawn _qtile_spawn_screen"

config.bind("X", "cmd-set-text -s :split")
config.bind("V", "cmd-set-text -s :vsplit", mode="normal")
config.bind("T", "cmd-set-text -s :tab")
config.bind("<Ctrl-T>", "cmd-set-text -s :tab_new")

# Qtile
config.bind(
    "Fv",
    "hint links spawn qtile cmd-obj -o layout -f spawn_split -a 'qb {hint-url}' x",
)
config.bind(
    "Fx",
    "hint links spawn qtile cmd-obj -o layout -f spawn_split -a 'qb {hint-url}' y",
)
config.bind(
    "Ft",
    "hint links spawn qtile cmd-obj -o layout -f spawn_tab -a 'qb {hint-url}'",
)
config.bind(
    "FT",
    "hint links spawn _qtile_spawn_new_tab '{hint-url}'",
)
config.bind(
    "Ff",
    "hint links spawn qtile cmd-obj -o root -f spawn -a 'qb {hint-url}'",
)

# Medias
config.bind("M", "hint links spawn mpv --x11-name='mpv-preview' {hint-url}")
# Navigation
config.bind("m", "mode-enter set_mark")

# Settings
config.bind("xb", "config-cycle statusbar.show never always")
config.bind(
    "xc",
    "config-cycle content.user_stylesheets ~/.config/qutebrowser/css/default.css ~/.config/qutebrowser/css/custom.css",
)
config.bind("xt", "config-cycle tabs.show multiple always")
