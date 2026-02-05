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
c.colors.webpage.darkmode.policy.images = "never"
c.input.insert_mode.auto_enter = False

c.content.user_stylesheets = "~/.config/qutebrowser/css/custom-onedark.css"
c.content.prefers_reduced_motion = True
c.downloads.location.directory = "/home/whammou/Downloads/"

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


# defaultSearxng = "https://opnxng.com"
defaultSearxng = "https://searx.namejeff.xyz/"
serxngQuery = defaultSearxng + "/search?q={}"
c.url.start_pages = ["https://ascii-start.customstart.page/"]
c.url.default_page = "https://ascii-start.customstart.page/"
c.url.searchengines = {
    # "DEFAULT": "https://opnxng.com/search?q={}",
    # "DEFAULT": "https://duckduckgo.com/?q={}",
    "DEFAULT": serxngQuery,
    "it": serxngQuery + "&categories=it",
    "vi": serxngQuery + "&categories=videos",
    "im": serxngQuery + "&categories=images",
    "ne": serxngQuery + "&categories=news",
    "ma": serxngQuery + "&categories=map",
    "mu": serxngQuery + "&categories=music",
    "sc": serxngQuery + "&categories=science",
    "fi": serxngQuery + "&categories=files",
    "so": serxngQuery + "&categories=social%20media",
    "bo": "https://annas-archive.li/search?q={}",
}

# c.fonts.default_size = "13pt"
