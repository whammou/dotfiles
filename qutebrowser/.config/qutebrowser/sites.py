# pylint: disable=C0111
from typing import Any
import json
import os
from lib.paths import CSS_DIR

# qutebrowser injects config when sourcing; globals()[...] binds it without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
config: Any = globals()["config"]

# user agent: {{{
config.set(
    "content.headers.user_agent",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "https://accounts.google.com/*",
)
# }}}

# darkmode: {{{
DARKMODE_SITES = [
    "https://github.com/*",
    "https://chat.zalo.me/",
    "https://chat.beeper.com/",
    *(f"https://{_suit}.google.com/*" for _suit in ("docs", "drive")),
    # "https://*.edu.vn/*",
]
for _site in DARKMODE_SITES:
    config.set("colors.webpage.darkmode.enabled", False, _site)
# }}}

# tabfreeze: domains never frozen, subdomains included {{{
os.environ["FREEZE_EXEMPT_DOMAINS"] = "chat.zalo.me,chat.beeper.com"
# }}}

# per-site css: host -> css module, subdomains included. tabcss.py appends
# the module to the base stylesheet bundle on matching hosts. Passed through
# the environment because qutebrowser purges sys.modules entries added while

# sourcing a config file, so no attribute survives from here. {{{
os.environ["SITE_CSS"] = json.dumps(
    {
        "youtube.com": CSS_DIR + "sites/youtube.css",
        "w3schools.com": CSS_DIR + "sites/w3schools.css",
        "github.com": CSS_DIR + "sites/github.css",
        "stackoverflow.com": CSS_DIR + "sites/stackoverflow.css",
        "news.ycombinator.com": CSS_DIR + "sites/news.ycombinator.com.css",
        "google.com": CSS_DIR + "sites/google.com.css",
    }
)
# }}}

# vim: foldmethod=marker foldlevel=0
