# pylint: disable=C0111
config = config  # noqa: F821 pylint: disable=E0602,C0103

config.set(
    "content.headers.user_agent",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
    "Gecko/20100101 Firefox/115.0",
    "https://accounts.google.com/*",
)
config.set("content.javascript.clipboard", "access-paste", "https://docs.github.com")
config.set("content.javascript.clipboard", "access-paste", "https://github.com")
config.set(
    "content.javascript.clipboard",
    "access-paste",
    "https://nvim-orgmode.github.io",
)
config.set("content.media.audio_capture", True, "https://meet.google.com")
config.set("content.media.audio_video_capture", True, "https://meet.google.com")
config.set("content.media.audio_video_capture", True, "https://teams.live.com")
config.set("content.media.video_capture", True, "https://meet.google.com")
config.set("content.notifications.enabled", True, "https://chat.zalo.me")
config.set("content.notifications.enabled", True, "https://meet.google.com")
config.set("content.notifications.enabled", True, "https://ntfy.whammou.dedyn.io")
config.set("content.notifications.enabled", True, "https://teams.live.com")
