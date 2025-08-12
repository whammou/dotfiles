# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103


# BROWSER SETTINGS
c.editor.command = ["kitty", "nvim", "{file}"]
c.search.wrap = False
c.new_instance_open_target = "tab-bg"
c.new_instance_open_target_window = "last-focused"
c.input.links_included_in_focus_chain = False
c.scrolling.bar = "when-searching"
c.scrolling.smooth = False
c.statusbar.show = "in-mode"
c.tabs.select_on_remove = "prev"
c.tabs.show = "multiple"
c.tabs.tabs_are_windows = True
c.colors.webpage.preferred_color_scheme = "dark"
c.colors.webpage.darkmode.enabled = True
c.input.insert_mode.auto_enter = False

c.content.user_stylesheets = "~/.config/qutebrowser/css/custom-onedark.css"
c.downloads.location.directory = "/home/whammou/downloads/"

c.fileselect.handler = "external"
c.fileselect.single_file.command = [
    "kitty",
    "--class",
    "fileselect",
    "-e",
    "yazi",
    "--chooser-file",
    "{}",
]
c.fileselect.multiple_files.command = [
    "kitty",
    "--class",
    "fileselect",
    "-e",
    "yazi",
    "--chooser-file",
    "{}",
]

c.completion.open_categories = [
    "searchengines",
    "quickmarks",
    "bookmarks",
    "filesystem",
]

c.url.start_pages = ["https://ascii-start.customstart.page/"]
c.url.default_page = "https://ascii-start.customstart.page/"
c.url.searchengines = {
    "DEFAULT": "https://opnxng.com/search?q={}",
    "gs": "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG=",
    "g": "https://www.google.com/search?q={}",
    "b": "https://search.brave.com/search?q={}",
    "y": "https://www.youtube.com/results?search_query={}",
    "wa": "https://wiki.archlinux.org/?search={}",
    "lg": "https://libgen.gs/index.php?req={}",
}

# c.fonts.default_size = "13pt"
