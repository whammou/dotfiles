config.load_autoconfig(True)
config.set('content.cookies.accept', 'all', 'chrome-devtools://*')
config.set('content.cookies.accept', 'all', 'devtools://*')
config.set('content.headers.accept_language', '', 'https://matchmaker.krunker.io/*')
config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version} Safari/{webkit_version}', 'https://web.whatsapp.com/')
config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}; rv:90.0) Gecko/20100101 Firefox/90.0', 'https://accounts.google.com/*')
config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99 Safari/537.36', 'https://*.slack.com/*')
config.set('content.images', True, 'chrome-devtools://*')
config.set('content.images', True, 'devtools://*')
config.set('content.javascript.enabled', True, 'chrome-devtools://*')
config.set('content.javascript.enabled', True, 'devtools://*')
config.set('content.javascript.enabled', True, 'chrome://*/*')
config.set('content.javascript.enabled', True, 'qute://*/*')
config.set('completion.open_categories', ["searchengines", "quickmarks", "bookmarks", "filesystem"])
config.set('scrolling.bar', 'when-searching')
config.set('zoom.default', 100)
config.set('fonts.web.size.default', 19)
config.set('qt.highdpi', True)
config.set('hints.border', '0px')
config.set('colors.webpage.darkmode.enabled', True)
config.set('statusbar.show', 'never')
config.set('tabs.show', 'never')
config.set('content.user_stylesheets', '/home/whammou/.config/qutebrowser/css/blackbg.css')
config.set('downloads.location.directory', '/home/whammou/.downloads/')

# Enable Theme
#config.source('qutebrowser-themes/themes/onedark.py')
config.source('/home/whammou/.config/qutebrowser/themes/mine.py')

# Enable Hardware Acceleration
config.set('qt.args',['ignore-gpu-blacklist','enable-gpu-rasterization','enable-native-gpu-memory-buffers','num-raster-threads=4'])

# Bindings for normal mode
config.bind('M', 'hint links spawn mpv --geometry=720x480 {hint-url}')
config.bind('xb', 'config-cycle statusbar.show never always')
config.bind('xt', 'config-cycle tabs.show never always')
config.bind('xc', "config-cycle content.user_stylesheets ~/.config/qutebrowser/css/blackbg.css ''")
config.bind('m', 'mode-enter set_mark')

# Configs for file picker
#config.set("fileselect.handler", "external")
#config.set("fileselect.single_file.command", ['alacritty','--title=ranger.ranger', '-e', 'ranger --choosefile {}'])
#config.set("fileselect.multiple_files.command", ['alacritty', '--title=ranger.ranger', '-e', 'ranger --choosefiles {}'])

# Set default search Engine and Startpage
c.url.searchengines = { "DEFAULT" : "https://opnxng.com/search?q={}", 
                       "gs" : "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG=",
                       "g" : "https://www.google.com/search?q={}",
                       "y" : "https://www.youtube.com/results?search_query={}",
                       "wa" : "https://wiki.archlinux.org/?search={}",
                       "lg" : "https://libgen.li/index.php?req={}"
                       }
c.url.start_pages = ['https://nimplex.github.io/Minimal-StartPage']
config.set('url.default_page', 'https://nimplex.github.io/Minimal-StartPage')

# Set Zotero add config
c.aliases['zotero'] = 'spawn --userscript zotero'
c.aliases['Zotero'] = 'hint links userscript zotero'
