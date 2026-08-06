# pylint: disable=C0111
from typing import Any

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# settings.py must be sourced before keys.py: the "xc" bind is built from
# c.content.user_stylesheets, which settings.py populates.
config.source("./daemon_keepalive.py")
config.source("./tabfreeze.py")
config.source("./themes/onedark-dark.py")
config.source("./settings.py")
config.source("./keys.py")
config.source("./tabcss.py")
config.source("./chromium.py")
config.source("./sites.py")
config.source("./fonts.py")

# autoconfig.yml is deliberately not loaded; its values were migrated to
# settings.py/sites.py, so re-enabling it would shadow those config values.
config.load_autoconfig(True)
