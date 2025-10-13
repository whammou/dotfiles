# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

# base16 colors but with variable names that
# reflect what the color is mainly used for

bg0 = "#1a212e"
bg1 = "#21283b"
bg2 = "#283347"
bg3 = "#2a324a"
grey = "#455574"
fg = "#93a4c3"
red = "#f65866"
yellow = "#efbd5c"
bg_yellow = "#f2cc81"
green = "#8bcd5b"
orange = "#dd9046"
cyan = "#34bfd0"
blue = "#41a7fc"
purple = "#c75ae8"


c.hints.border = "0px"
c.hints.radius = 0
c.fonts.hints = "default_size default_family"

c.fonts.default_size = "13pt"
c.fonts.web.size.default = 19
c.colors.webpage.preferred_color_scheme = "dark"

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
c.colors.contextmenu.disabled.bg = bg1
c.colors.contextmenu.disabled.fg = grey
c.colors.contextmenu.menu.bg = bg0
c.colors.contextmenu.menu.fg = fg
c.colors.contextmenu.selected.bg = bg2
c.colors.contextmenu.selected.fg = fg
c.colors.downloads.bar.bg = bg0
c.colors.downloads.start.fg = bg0
c.colors.downloads.start.bg = blue
c.colors.downloads.stop.fg = bg0
c.colors.downloads.stop.bg = cyan
c.colors.downloads.error.fg = red
c.colors.hints.fg = grey

# Background color for hints. Note that you can use a `rgba(...)` value
# for transparency.
c.colors.hints.bg = green
c.colors.hints.match.fg = green
c.colors.keyhint.fg = grey
c.colors.keyhint.suffix.fg = fg
c.colors.keyhint.bg = bg0
c.colors.messages.error.fg = bg0
c.colors.messages.error.bg = red
c.colors.messages.error.border = red
c.colors.messages.warning.fg = bg0
c.colors.messages.warning.bg = purple
c.colors.messages.warning.border = purple
c.colors.messages.info.fg = fg
c.colors.messages.info.bg = bg0
c.colors.messages.info.border = bg0
c.colors.prompts.fg = fg
c.colors.prompts.border = bg0
c.colors.prompts.bg = bg0
c.colors.prompts.selected.bg = bg2
c.colors.prompts.selected.fg = fg
c.colors.statusbar.normal.fg = green
c.colors.statusbar.normal.bg = bg0
c.colors.statusbar.insert.fg = blue
c.colors.statusbar.insert.bg = bg3
c.colors.statusbar.passthrough.fg = cyan
c.colors.statusbar.passthrough.bg = bg3
c.colors.statusbar.private.fg = bg0
c.colors.statusbar.private.bg = bg1
c.colors.statusbar.command.fg = fg
c.colors.statusbar.command.bg = bg0
c.colors.statusbar.command.private.fg = fg
c.colors.statusbar.command.private.bg = bg0
c.colors.statusbar.caret.fg = purple
c.colors.statusbar.caret.bg = bg3
c.colors.statusbar.caret.selection.fg = blue
c.colors.statusbar.caret.selection.bg = bg3
c.colors.statusbar.progress.bg = blue
c.colors.statusbar.url.fg = fg
c.colors.statusbar.url.error.fg = red
c.colors.statusbar.url.hover.fg = fg
c.colors.statusbar.url.success.http.fg = cyan
c.colors.statusbar.url.success.https.fg = green
c.colors.statusbar.url.warn.fg = purple
c.colors.tabs.bar.bg = bg0
c.colors.tabs.indicator.start = blue
c.colors.tabs.indicator.stop = cyan
c.colors.tabs.indicator.error = red
c.colors.tabs.odd.fg = fg
c.colors.tabs.odd.bg = bg1
c.colors.tabs.even.fg = fg
c.colors.tabs.even.bg = bg0
c.colors.tabs.pinned.even.bg = cyan
c.colors.tabs.pinned.even.fg = bg3
c.colors.tabs.pinned.odd.bg = green
c.colors.tabs.pinned.odd.fg = bg3
c.colors.tabs.pinned.selected.even.bg = bg2
c.colors.tabs.pinned.selected.even.fg = fg
c.colors.tabs.pinned.selected.odd.bg = bg2
c.colors.tabs.pinned.selected.odd.fg = fg
c.colors.tabs.selected.odd.fg = fg
c.colors.tabs.selected.odd.bg = bg2
c.colors.tabs.selected.even.fg = fg
c.colors.tabs.selected.even.bg = bg2
# c.colors.webpage.bg = bg0
