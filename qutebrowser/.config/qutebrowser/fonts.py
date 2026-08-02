from typing import Any

# qutebrowser injects c when sourcing; globals()[...] binds it without
# self-assignment or undefined names, keeping ruff/pyflakes/pyright quiet.
c: Any = globals()["c"]

c.fonts.web.family.cursive = "HasklugNerdFont"
c.fonts.web.family.fantasy = "HasklugNerdFont"
c.fonts.web.family.fixed = "HasklugNerdFont"
c.fonts.web.family.sans_serif = "HasklugNerdFont"
c.fonts.web.family.serif = "HasklugNerdFont"
c.fonts.web.family.standard = "HasklugNerdFont"
