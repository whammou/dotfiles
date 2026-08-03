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

# javascript.clipboard: {{{
config.set("content.javascript.clipboard", "access-paste", "https://docs.github.com")  # noqa: E501
config.set("content.javascript.clipboard", "access-paste", "https://github.com")  # noqa: E501
config.set(
    "content.javascript.clipboard",
    "access-paste",
    "https://nvim-orgmode.github.io",
)
# }}}

# media capture: {{{
config.set("content.media.audio_capture", True, "https://meet.google.com")
config.set("content.media.audio_video_capture", True, "https://meet.google.com")  # noqa: E501
config.set("content.media.audio_video_capture", True, "https://teams.live.com")
config.set("content.media.video_capture", True, "https://meet.google.com")
# }}}

# notifications: {{{
config.set("content.notifications.enabled", True, "https://chat.zalo.me")
config.set("content.notifications.enabled", True, "https://meet.google.com")
config.set("content.notifications.enabled", True, "https://ntfy.whammou.dedyn.io")  # noqa: E501
config.set("content.notifications.enabled", True, "https://teams.live.com")
# }}}

# darkmode: {{{
DARKMODE_SITES = [
    *(f"https://*.rmit.edu.{_tld}/*" for _tld in ("vn", "au")),
    "https://*.wikipedia.org/*",
    # "https://*.edu.vn/*",
]
for _site in DARKMODE_SITES:
    config.set("colors.webpage.darkmode.enabled", True, _site)
# }}}
# vim: foldmethod=marker foldlevel=0
