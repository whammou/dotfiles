# pylint: disable=C0111
from typing import Any

# qutebrowser injects c when sourcing; globals()[...] binds it without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]

# palette: {{{
# base16 colors but with variable names that
# reflect what the color is mainly used for

# Backgrounds (neutral)
black = "#181a1f"
bg0 = "#282c34"
bg1 = "#31353f"
bg2 = "#393f4a"
bg3 = "#3b3f4c"
bg_d = "#21252b"
bg_blue = "#73b8f1"
bg_yellow = "#ebd09c"

# Foreground (text)
fg = "#abb2bf"
grey = "#5c6370"
light_grey = "#848b98"

# Accent Colors - Bright
red = "#e86671"
yellow = "#e5c07b"
green = "#98c379"
orange = "#d19a66"
cyan = "#56b6c2"
blue = "#61afef"
purple = "#c678dd"

# Accent Colors - Dark (palette.lua)
dark_cyan = "#2b6f77"
dark_red = "#993939"
dark_yellow = "#93691d"
dark_purple = "#8a3fa0"

# Accent Colors - Tinted backgrounds (colorscheme.lua tbg_*)
tbg_red = "#884953"
tbg_green = "#607857"
tbg_blue = "#456E92"
tbg_purple = "#775289"
tbg_cyan = "#3F717B"
tbg_yellow = "#877658"
tbg_orange = "#6e594f"
tbg_grey = "#5c6370"

# Dimmed Colors - subtle backgrounds (colorscheme.lua)
dimmed_red = "#3e323a"
dimmed_green = "#333d39"
dimmed_yellow = "#3d3c39"
dimmed_blue = "#2c3949"
dimmed_purple = "#393247"
dimmed_cyan = "#2b3c44"
dimmed_orange = "#3c3736"

# Diff/Syntax Colors (palette.lua)
diff_add = "#31392b"
diff_delete = "#382b2c"
diff_change = "#1c3448"
diff_text = "#2c5372"
# }}}

# fonts: {{{
c.fonts.default_size = "13pt"
c.fonts.web.size.default = 19
# }}}

# hints: {{{
c.hints.border = "0px"
c.hints.radius = 0
c.hints.padding = {"top": 2, "bottom": 2, "left": 4, "right": 4}
c.fonts.hints = "default_size default_family"
c.colors.hints.fg = grey
# Background color for hints. Note that you can use a `rgba(...)` value
# for transparency.
c.colors.hints.bg = green
c.colors.hints.match.fg = green
# }}}

# webpage: {{{
c.colors.webpage.preferred_color_scheme = "dark"
# c.colors.webpage.bg = bg0
# }}}

# completion: {{{
# Text color of the completion widget. May be a single color to use for
# all columns or a list of three colors, one for each column.
c.colors.completion.fg = fg
c.colors.completion.odd.bg = bg1
c.colors.completion.even.bg = bg0
c.colors.completion.category.fg = yellow
c.colors.completion.category.bg = bg0
c.colors.completion.category.border.top = bg0
c.colors.completion.category.border.bottom = bg0
c.colors.completion.item.selected.fg = fg
c.colors.completion.item.selected.bg = bg2
c.colors.completion.item.selected.border.top = bg2
c.colors.completion.item.selected.border.bottom = bg2
c.colors.completion.item.selected.match.fg = green
c.colors.completion.match.fg = green
c.colors.completion.scrollbar.fg = fg
c.colors.completion.scrollbar.bg = bg0
# }}}

# contextmenu: {{{
c.colors.contextmenu.disabled.bg = bg1
c.colors.contextmenu.disabled.fg = grey
c.colors.contextmenu.menu.bg = bg0
c.colors.contextmenu.menu.fg = fg
c.colors.contextmenu.selected.bg = bg2
c.colors.contextmenu.selected.fg = fg
# }}}

# downloads: {{{
c.colors.downloads.bar.bg = bg0
c.colors.downloads.start.fg = bg0
c.colors.downloads.start.bg = blue
c.colors.downloads.stop.fg = bg0
c.colors.downloads.stop.bg = cyan
c.colors.downloads.error.fg = red
# }}}

# keyhint: {{{
c.colors.keyhint.fg = grey
c.colors.keyhint.suffix.fg = fg
c.colors.keyhint.bg = bg0
# }}}

# messages: {{{
c.colors.messages.error.fg = bg0
c.colors.messages.error.bg = red
c.colors.messages.error.border = red
c.colors.messages.warning.fg = bg0
c.colors.messages.warning.bg = purple
c.colors.messages.warning.border = purple
c.colors.messages.info.fg = bg0
c.colors.messages.info.bg = blue
c.colors.messages.info.border = bg0
# }}}

# prompts: {{{
c.colors.prompts.fg = fg
c.colors.prompts.border = bg0
c.colors.prompts.bg = bg0
c.colors.prompts.selected.bg = bg2
c.colors.prompts.selected.fg = fg
# }}}

# statusbar: {{{
c.colors.statusbar.normal.fg = green
c.colors.statusbar.normal.bg = bg0
c.colors.statusbar.insert.fg = blue
c.colors.statusbar.insert.bg = bg_d
c.colors.statusbar.passthrough.fg = cyan
c.colors.statusbar.passthrough.bg = bg_d
c.colors.statusbar.private.fg = bg0
c.colors.statusbar.private.bg = bg1
c.colors.statusbar.command.fg = fg
c.colors.statusbar.command.bg = bg_d
c.colors.statusbar.command.private.fg = fg
c.colors.statusbar.command.private.bg = bg0
c.colors.statusbar.caret.fg = purple
c.colors.statusbar.caret.bg = bg_d
c.colors.statusbar.caret.selection.fg = blue
c.colors.statusbar.caret.selection.bg = bg_d
c.colors.statusbar.progress.bg = blue
c.colors.statusbar.url.fg = fg
c.colors.statusbar.url.error.fg = red
c.colors.statusbar.url.hover.fg = fg
c.colors.statusbar.url.success.http.fg = cyan
c.colors.statusbar.url.success.https.fg = green
c.colors.statusbar.url.warn.fg = purple
# }}}

# tabs: {{{
c.colors.tabs.bar.bg = bg0
c.colors.tabs.indicator.start = blue
c.colors.tabs.indicator.stop = cyan
c.colors.tabs.indicator.error = red
c.colors.tabs.odd.fg = fg
c.colors.tabs.odd.bg = bg1
c.colors.tabs.even.fg = fg
c.colors.tabs.even.bg = bg0
c.colors.tabs.pinned.even.bg = cyan
c.colors.tabs.pinned.even.fg = bg_d
c.colors.tabs.pinned.odd.bg = green
c.colors.tabs.pinned.odd.fg = bg_d
c.colors.tabs.pinned.selected.even.bg = bg2
c.colors.tabs.pinned.selected.even.fg = fg
c.colors.tabs.pinned.selected.odd.bg = bg2
c.colors.tabs.pinned.selected.odd.fg = fg
c.colors.tabs.selected.odd.fg = fg
c.colors.tabs.selected.odd.bg = bg2
c.colors.tabs.selected.even.fg = fg
c.colors.tabs.selected.even.bg = bg2
# }}}
# vim: foldmethod=marker foldlevel=0
