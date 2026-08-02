# pylint: disable=C0111
import glob
import os
from typing import Any

from paths import CSS_DIR

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# BROWSER SETTINGS
# c.editor.command = ["kitty", "nvim", "{file}"]
c.window.title_format = "QB | [{scroll_pos}] {audio}{current_title}{title_sep}{host}"  # noqa: E501
c.editor.command = [
    "/home/whammou/.config/qutebrowser/userscripts/editor-wrapper.py",
    "{file}",
    "{line}",
    "{column}",
]
c.completion.show = "auto"
c.search.wrap = False
c.new_instance_open_target = "tab-bg"
c.new_instance_open_target_window = "last-focused"
c.input.links_included_in_focus_chain = False
c.scrolling.bar = "never"
c.scrolling.smooth = False
c.content.cache.size = 512000
c.content.geolocation = False
c.content.notifications.enabled = False
c.statusbar.show = "never"
c.tabs.select_on_remove = "prev"
c.tabs.show = "multiple"
c.tabs.tabs_are_windows = True
c.colors.webpage.preferred_color_scheme = "dark"
c.colors.webpage.darkmode.algorithm = "brightness-rgb"
c.colors.webpage.darkmode.enabled = False
c.colors.webpage.darkmode.policy.images = "smart-simple"
c.colors.webpage.darkmode.policy.page = "smart"
c.input.insert_mode.auto_enter = False

# All css files, ordered by numeric filename prefix (00- ... 99-);
# default.css is an empty placeholder and intentionally excluded.
c.content.user_stylesheets = [
    p
    for p in sorted(glob.glob(os.path.expanduser(CSS_DIR) + "*.css"))
    if os.path.basename(p) != "default.css"
]

# "xc" toggles stylesheets off/on; the on-state is built from the list above
# so the bind can never drift from the actual css files (single source of truth).  # noqa: E501
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

c.completion.shrink = True
c.content.blocking.enabled = True
c.content.headers.user_agent = (
    "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
    "{upstream_browser_key}/{upstream_browser_version_short} Safari/{webkit_version}"  # noqa: E501
)
c.content.javascript.enabled = True
c.window.hide_decoration = False

c.completion.open_categories = [
    "searchengines",
    "quickmarks",
    "bookmarks",
    "filesystem",
]


searxngInstance = "https://opnxng.com"
google = "https://google.com/search?q={}"
# searxngInstance = "https://searx.namejeff.xyz/"
# searxngInstance = "https://search.hbubli.cc/"
searxngQuery = searxngInstance + "/search?q={}"
searxngSearch = {
    "DEFAULT": google,
    "xi": searxngQuery + "&categories=it",
    "xv": searxngQuery + "&categories=videos",
    "xm": searxngQuery + "&categories=images",
    "xn": searxngQuery + "&categories=news",
    "xa": searxngQuery + "&categories=map",
    "xu": searxngQuery + "&categories=music",
    "xc": searxngQuery + "&categories=science",
    "xf": searxngQuery + "&categories=files",
    "xs": searxngQuery + "&categories=social%20media",
    "xx": searxngQuery,
    "aa": "https://annas-archive.li/search?q={}",
    "gg": "https://www.google.com/search?q={}",
    "bb": "https://search.brave.com/search?q={}",
}

c.url.start_pages = ["https://ascii-start.customstart.page/"]
c.url.default_page = "https://ascii-start.customstart.page/"
c.url.searchengines = searxngSearch

# c.fonts.default_size = "13pt"
