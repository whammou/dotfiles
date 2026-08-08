# pylint: disable=C0111
from pathlib import Path
from typing import Any

# qutebrowser injects c/config when sourcing; globals()[...] binds them without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]
config: Any = globals()["config"]

# Module layout: the files sourced below run in qutebrowser's injected
# namespace (`c`, `config` available). Pure helpers (lib/paths.py,
# lib/minicss.py) are NEVER sourced here — they are imported via regular
# import machinery by the sourced modules and must stay free of the injected
# globals; sys.modules entries they add are purged after each source, which is
# harmless because they are pure.

# settings.py must be sourced before keys.py: the "xc" bind is built from
# c.content.user_stylesheets, which settings.py populates.

# addons: every *.py in addons/ is sourced automatically, sorted by name.
# These are runtime-hook modules (daemon_keepalive, tabfreeze, pinnedtitle,
# tabcss); they arm via daemon threads once the app exists, so their order
# relative to the config-value files below does not matter. Drop a new module
# into addons/ to source it.
_addons_dir = Path(__file__).resolve().parent / "addons"
for _addon in sorted(_addons_dir.glob("*.py")):
    config.source(str(_addon))

config.source("./themes/onedark-dark.py")
config.source("./settings.py")
config.source("./keys.py")
config.source("./chromium.py")
config.source("./sites.py")
config.source("./fonts.py")

# autoconfig.yml is deliberately not loaded; its values were migrated to
# settings.py/sites.py, so re-enabling it would shadow those config values.
config.load_autoconfig(True)
