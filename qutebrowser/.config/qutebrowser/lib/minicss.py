# minicss.py - comment-stripped copies of the stylesheet bundle.
#
# Pure module (no qutebrowser injected globals), same constraint as paths.py:
# qutebrowser purges sys.modules entries added while sourcing config files,
# and regular re-imports just re-execute this file, so it must stay free of
# side effects beyond the cache writes.

import glob
import os

from lib.paths import CSS_DIR

CACHE_DIR = "~/.cache/qutebrowser/css/"


def strip_comments(css: str) -> str:
    """Drop /* ... */ comments; quoted strings are left untouched."""
    out: list[str] = []
    i = 0
    n = len(css)
    quote = ""
    while i < n:
        ch = css[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(css[i + 1])
                i += 2
            else:
                if ch == quote:
                    quote = ""
                i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            out.append(ch)
            i += 1
        elif ch == "/" and i + 1 < n and css[i + 1] == "*":
            end = css.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def bundle() -> list[str]:
    """Paths of minified copies of css/*.css (default.css excluded), rebuilt
    when a source is newer; original paths are returned when writing fails."""
    sources = [
        p
        for p in sorted(glob.glob(os.path.expanduser(CSS_DIR) + "*.css"))
        if os.path.basename(p) != "default.css"
    ]
    try:
        cache = os.path.expanduser(CACHE_DIR)
        os.makedirs(cache, exist_ok=True)
    except OSError:
        return sources
    paths = []
    for src in sources:
        dst = os.path.join(cache, os.path.basename(src))
        try:
            if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                with open(src, encoding="utf-8") as f:
                    css = strip_comments(f.read())
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(css)
            paths.append(dst)
        except OSError:
            paths.append(src)
    return paths
