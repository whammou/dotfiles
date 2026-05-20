# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103


# BROWSER SETTINGS
# c.editor.command = ["kitty", "nvim", "{file}"]
c.editor.command = [
    "kitty",
    "--single-instance",
    "--app-id",
    "kitty-float",
    "nvim",
    "{file}",
    "+startinsert",
    "+call cursor({line}, {column})",
]
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

c.content.proxy = "socks5://127.0.0.1:1080"
c.content.tls.certificate_errors = "ask-block-thirdparty"
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


searxngInstance = "https://opnxng.com"
# searxngInstance = "https://searx.namejeff.xyz/"
# searxngInstance = "https://search.hbubli.cc/"
searxngQuery = searxngInstance + "/search?q={}"
searxngSearch = {
    "DEFAULT": searxngQuery,
    "xi": searxngQuery + "&categories=it",
    "xv": searxngQuery + "&categories=videos",
    "xm": searxngQuery + "&categories=images",
    "xn": searxngQuery + "&categories=news",
    "xa": searxngQuery + "&categories=map",
    "xu": searxngQuery + "&categories=music",
    "xc": searxngQuery + "&categories=science",
    "xf": searxngQuery + "&categories=files",
    "xs": searxngQuery + "&categories=social%20media",
    "aa": "https://annas-archive.li/search?q={}",
    "gg": "https://www.google.com/search?q={}",
    "bb": "https://search.brave.com/search?q={}",
}

c.url.start_pages = ["https://ascii-start.customstart.page/"]
c.url.default_page = "https://ascii-start.customstart.page/"
c.url.searchengines = searxngSearch

# c.fonts.default_size = "13pt"
