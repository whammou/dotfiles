# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103


c.qt.args = [
    "ignore-gpu-blacklist",
    "enable-gpu-rasterization",
    "enable-native-gpu-memory-buffers",
    "enable-zero-copy",
    "gtk-version=4",
    "enable-features=VaapiVideoEncoder,VaapiVideoDecoder,CanvasOopRasterization,VaapiIgnoreDriverChecks,PlatformHEVCDecoderSupport,UseMultiPlaneFormatForHardwareVideo",
    "num-raster-threads=4",
    "use-gl desktop",
    "enable-accelerated-2d-canvas",
    "enable-accelerated-video-decode",
    "disable-gpu-sandbox",
    "content.prefers_reduced_motion",
]

c.qt.workarounds.disable_accelerated_2d_canvas = "never"
c.qt.workarounds.disable_hangouts_extension = True
c.qt.workarounds.disable_accessibility = "always"

c.content.autoplay = False
config.set("content.cookies.accept", "all", "chrome-devtools://*")
config.set("content.cookies.accept", "all", "devtools://*")
config.set("content.headers.accept_language", "", "https://matchmaker.krunker.io/*")
c.content.headers.user_agent = "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version_short} Safari/{webkit_version}"
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
