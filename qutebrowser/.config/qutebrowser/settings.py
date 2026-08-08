# pylint: disable=C0111
from typing import Any

from lib.minicss import bundle

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# window: {{{
c.window.title_format = "QB | {audio}{current_title}{title_sep}{host}"  # noqa: E501
c.window.hide_decoration = False
# }}}

# editor: {{{
# c.editor.command = ["kitty", "nvim", "{file}"]
c.editor.command = [
    "/home/whammou/.config/qutebrowser/userscripts/editor-wrapper.py",
    "{file}",
    "{line}",
    "{column}",
]
# }}}

# fileselect: {{{
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
# }}}

# completion: {{{
c.completion.show = "auto"
c.completion.shrink = True
c.completion.open_categories = [
    "searchengines",
    "quickmarks",
    "bookmarks",
    "filesystem",
]
# }}}

# tabs: {{{
c.tabs.select_on_remove = "prev"
c.tabs.show = "multiple"
c.tabs.tabs_are_windows = True
c.new_instance_open_target = "tab-bg"
c.new_instance_open_target_window = "last-focused"
# }}}

# input: {{{
c.input.links_included_in_focus_chain = False
c.input.insert_mode.auto_enter = False
# }}}

# scrolling: {{{
c.scrolling.bar = "overlay"
c.scrolling.smooth = False
# }}}

# search: {{{
c.search.wrap = False
# }}}

# statusbar: {{{
c.statusbar.show = "never"
# }}}

# content: {{{
c.content.blocking.enabled = True
c.content.cache.size = 512000
c.content.geolocation = False
c.content.headers.user_agent = (
    "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
    "{upstream_browser_key}/{upstream_browser_version_short} Safari/{webkit_version}"  # noqa: E501
)
c.content.javascript.enabled = True
c.content.notifications.enabled = False
c.content.prefers_reduced_motion = True
# Per-site proxy: QtWebEngine has no per-site proxy support (no setHttpProxy
# in PyQt6 6.11, PAC unimplemented on QtWebEngine, CLI proxy flags ignored),
# so proxysplit.py (started by qutebrowser-daemon) routes the dev server
# through the hysteria tunnel and everything else directly; QtWebEngine is
# fed this single global proxy via the application QNetworkProxyFactory.
# c.content.proxy = "socks5://127.0.0.1:1081"
c.content.proxy = "system"
c.content.tls.certificate_errors = "ask-block-thirdparty"
# }}}

# darkmode: {{{
c.colors.webpage.preferred_color_scheme = "dark"
c.colors.webpage.darkmode.algorithm = "brightness-rgb"
c.colors.webpage.darkmode.enabled = True
c.colors.webpage.darkmode.policy.images = "never"
c.colors.webpage.darkmode.policy.page = "smart"
# }}}

# stylesheets: {{{
# All css files, ordered by numeric filename prefix (00- ... 99-);
# default.css is an empty placeholder and intentionally excluded. minicss
# serves comment-stripped copies (~4KB lighter) from the cache dir.
c.content.user_stylesheets = bundle()

# "xc" toggles stylesheets off/on; the on-state is built from the list above
# so the bind can never drift from the actual css files (single source of truth).  # noqa: E501
# }}}

# download: {{{
c.downloads.location.directory = "/home/whammou/Downloads/"
# }}}

# searchengines: {{{
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
c.url.searchengines = searxngSearch
# }}}

# url: {{{
c.url.start_pages = ["https://ascii-start.customstart.page/"]
c.url.default_page = "https://ascii-start.customstart.page/"
# }}}

# fonts: {{{
# c.fonts.default_size = "13pt"
# }}}
# vim: foldmethod=marker foldlevel=0
