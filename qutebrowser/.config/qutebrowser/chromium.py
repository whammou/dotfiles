# pylint: disable=C0111
from typing import Any

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]


c.qt.args = [
    "enable-gpu-rasterization",
    "enable-native-gpu-memory-buffers",
    "enable-zero-copy",
    "gtk-version=4",
    "enable-features=VaapiVideoEncoder,VaapiVideoDecoder,CanvasOopRasterization,VaapiIgnoreDriverChecks,PlatformHEVCDecoderSupport,UseMultiPlaneFormatForHardwareVideo,WebRTCPipeWireCapturer,NetworkPrediction,PrefetchPrivacyChanges,DirectCompositing,EnableRawDraw",  # noqa: E501
    "num-raster-threads=4",
    "use-gl desktop",
    "enable-accelerated-2d-canvas",
    "enable-accelerated-video-decode",
    "enable-quic",
]

c.qt.chromium.process_model = "process-per-site"
c.qt.workarounds.disable_accelerated_2d_canvas = "never"
c.qt.workarounds.disable_hangouts_extension = True
c.qt.workarounds.disable_accessibility = "always"

c.content.autoplay = False
config.set("content.cookies.accept", "all", "chrome-devtools://*")
config.set("content.cookies.accept", "all", "devtools://*")
config.set("content.headers.accept_language", "", "https://matchmaker.krunker.io/*")  # noqa: E501
c.content.headers.user_agent = "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version_short} Safari/{webkit_version}"  # noqa: E501
# Global Accept override removed: a static text/html Accept breaks image CDNs
# (e.g. preview.redd.it) which require image/webp,image/*; QtWebEngine sends
# the correct per-resource Accept automatically (text/html for docs, image/* for images).
c.content.headers.custom = {}
config.set("content.javascript.enabled", True, "chrome-devtools://*")
config.set("content.javascript.enabled", True, "devtools://*")
config.set("content.javascript.enabled", True, "chrome://*/*")
config.set("content.javascript.enabled", True, "qute://*/*")
config.set(
    "content.local_content_can_access_remote_urls",
    True,
    "file:///home/whammou/.local/share/qutebrowser/userscripts/*",
)
config.set(
    "content.local_content_can_access_file_urls",
    False,
    "file:///home/whammou/.local/share/qutebrowser/userscripts/*",
)
