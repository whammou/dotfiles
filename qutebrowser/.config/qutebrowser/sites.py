# pylint: disable=C0111
from typing import Any

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
import os
os.environ["FREEZE_EXEMPT_DOMAINS"] = "chat.zalo.me,chat.beeper.com"
# }}}

# vim: foldmethod=marker foldlevel=0
