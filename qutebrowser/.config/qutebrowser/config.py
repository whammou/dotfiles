# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

config.source("./daemon_keepalive.py")
config.source("./themes/onedark-dark.py")
config.source("./keys.py")
config.source("./tabcss.py")
config.source("./chromium.py")
config.source("./settings.py")
config.source("./sites.py")
config.source("./fonts.py")

# autoconfig.yml is deliberately not loaded; its values were migrated to
# settings.py/sites.py, so re-enabling it would shadow those config values.

