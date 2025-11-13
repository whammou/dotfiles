# pylint: disable=C0111
import os
from urllib.request import urlopen

c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103
# load your autoconfig, use this, if the rest of your config is empty!

config.load_autoconfig()

if not os.path.exists(config.configdir / "theme.py"):
    theme = "https://raw.githubusercontent.com/catppuccin/qutebrowser/main/setup.py"
    with urlopen(theme) as themehtml:
        with open(config.configdir / "theme.py", "a") as file:
            file.writelines(themehtml.read().decode("utf-8"))

if os.path.exists(config.configdir / "theme.py"):
    import theme

    theme.setup(c, "macchiato", True)


config.source("./keys.py")
config.source("./chromium.py")
config.source("./settings.py")

config.load_autoconfig(True)
