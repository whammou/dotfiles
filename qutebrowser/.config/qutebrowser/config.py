config.load_autoconfig(True)

# Enable Hardware Acceleration
config.set(
    "qt.args",
    [
        "ignore-gpu-blacklist",
        "enable-gpu-rasterization",
        "enable-native-gpu-memory-buffers",
        "num-raster-threads=4",
        "use-gl desktop",
        "enable-accelerated-2d-canvas",
        "enable-accelerated-video-decode",
    ],
)

# Enable Theme
config.source("/home/whammou/.config/qutebrowser/themes/onedark.py")

# Default start-page
c.url.start_pages = ["https://nimplex.github.io/Minimal-StartPage"]
config.set("url.default_page", "https://nimplex.github.io/Minimal-StartPage")

# Bindings for normal mode
config.bind("M", "hint links spawn mpv --x11-name='mpv-preview' {hint-url}")
config.bind("xb", "config-cycle statusbar.show never always")
config.bind("m", "mode-enter set_mark")
config.bind("xt", "config-cycle tabs.show multiple always")
config.bind(
    "xc",
    "config-cycle content.user_stylesheets ~/.config/qutebrowser/css/default.css ~/.config/qutebrowser/css/custom.css",
)
config.set("new_instance_open_target", "tab-bg")
config.set("new_instance_open_target_window", "last-focused")
config.set("tabs.tabs_are_windows", True)

# Set default search Engine
c.url.searchengines = {
    "DEFAULT": "https://opnxng.com/search?q={}",
    "gs": "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG=",
    "g": "https://www.google.com/search?q={}",
    "y": "https://www.youtube.com/results?search_query={}",
    "wa": "https://wiki.archlinux.org/?search={}",
    "lg": "https://libgen.li/index.php?req={}",
}
config.set("search.wrap", False)

config.set("content.cookies.accept", "all", "chrome-devtools://*")
config.set("content.cookies.accept", "all", "devtools://*")

# config.set("qt.chromium.process_model", "process-per-site")
config.set("qt.workarounds.disable_accelerated_2d_canvas", "never")

config.set("content.images", True, "chrome-devtools://*")
config.set("content.images", True, "devtools://*")

config.set("content.javascript.enabled", True, "chrome-devtools://*")
config.set("content.javascript.enabled", True, "devtools://*")
config.set("content.javascript.enabled", True, "chrome://*/*")
config.set("content.javascript.enabled", True, "qute://*/*")

config.set(
    "completion.open_categories",
    ["searchengines", "quickmarks", "bookmarks", "filesystem"],
)

config.set("scrolling.bar", "when-searching")
config.set("statusbar.show", "never")
config.set("hints.radius", 0)
config.set("tabs.show", "multiple")
config.set("content.user_stylesheets", "~/.config/qutebrowser/css/custom.css")

config.set("fonts.web.size.default", 19)
config.set("hints.border", "0px")
config.set("colors.webpage.darkmode.enabled", True)
config.set("content.autoplay", False)

config.set("downloads.location.directory", "/home/whammou/.downloads/")


# Configs for file picker
# config.set("fileselect.handler", "external")
# config.set("fileselect.single_file.command", ['alacritty','--title=ranger.ranger', '-e', 'ranger --choosefile {}'])
# config.set("fileselect.multiple_files.command", ['alacritty', '--title=ranger.ranger', '-e', 'ranger --choosefiles {}'])


# Set Zotero add config
# c.aliases["zotero"] = "spawn --userscript zotero"
# c.aliases["Zotero"] = "hint links userscript zotero"

# config.set("content.headers.accept_language", "", "https://matchmaker.krunker.io/*")
# config.set(
#    "content.headers.user_agent",
#    "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version} Safari/{webkit_version}",
#    "https://web.whatsapp.com/",
# )
# config.set(
#    "content.headers.user_agent",
#    "Mozilla/5.0 ({os_info}; rv:90.0) Gecko/20100101 Firefox/90.0",
#    "https://accounts.google.com/*",
# )
# config.set(
#    "content.headers.user_agent",
#    "Mozilla/5.0 ({os_info}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99 Safari/537.36",
#    "https://*.slack.com/*",
# )
