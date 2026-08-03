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
    *(f"https://*.rmit.edu.{_tld}/*" for _tld in ("vn", "au")),
    *(f"https://{_suit}.google.com/*" for _suit in ("mail", "docs", "meet")),
    "https://www.google.com/maps/*",
    "https://*.wikipedia.org/*",
    # "https://*.edu.vn/*",
]
for _site in DARKMODE_SITES:
    config.set("colors.webpage.darkmode.enabled", True, _site)
# }}}

# vim: foldmethod=marker foldlevel=0
