#!/usr/bin/env python3
"""Export qutebrowser cookies to Netscape cookies.txt for yt-dlp.

qutebrowser stores its cookie database (Chromium SQLite format) at
~/.local/share/qutebrowser/webengine/Cookies. Unlike Google Chrome, qutebrowser
stores cookie *values* in plaintext (encrypted_value is empty), so a simple
stdlib-only conversion suffices.

Usage:
    export-qutebrowser-cookies.py [OUTPUT_PATH]

Writes a Netscape-format cookies.txt (the format yt-dlp's --cookies expects),
defaulting to /tmp/qutebrowser-cookies.txt. The .txt file is only read by
yt-dlp at fetch time, so running this just before mpv launch keeps auth fresh.
"""

import os
import sqlite3
import sys
from pathlib import Path

# Chromium timestamps are microseconds since 1601-01-01 UTC (Windows epoch).
# Unix epoch is 1970-01-01. Difference = 11644473600 seconds.
WINDOWS_TO_UNIX = 11644473600


def convert(profile_dir: Path, out_path: Path) -> int:
    db_path = profile_dir / "webengine" / "Cookies"
    if not db_path.exists():
        print(f"cookie DB not found: {db_path}", file=sys.stderr)
        return 1

    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = db.execute(
            """
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
            FROM cookies
            WHERE is_persistent = 1 AND host_key != ''
            """
        ).fetchall()
    finally:
        db.close()

    # Netscape cookies.txt uses TAB separators. Field order:
    # domain \t include_subdomains(TRUE/FALSE) \t path \t secure(TRUE/FALSE)
    #   \t expiry(unix) \t name \t value
    #
    # Consistency requirement (enforced by http.cookiejar._really_load):
    #   include_subdomains == domain.startswith(".")
    # So a domain-scoped cookie (host_key with leading '.') must carry TRUE and
    # keep its leading dot:  .youtube.com  TRUE. A host-only cookie (host_key
    # without leading dot) must carry FALSE and stay bare:  www.example.com FALSE.
    lines = ["# Netscape HTTP Cookie File", "# Generated from qutebrowser by export-qutebrowser-cookies.py"]
    for host, name, value, path, expires_utc, is_secure, is_httponly in rows:
        if host.startswith("."):
            include_sub = "TRUE"
            domain = host  # keep leading dot for domain-scoped cookies
        else:
            include_sub = "FALSE"
            domain = host

        if expires_utc and expires_utc > 0:
            expiry = max(0, (expires_utc // 1_000_000) - WINDOWS_TO_UNIX)
        else:
            # Session cookie / no expiry -> keep as 0 (expires at end of session).
            expiry = 0

        lines.append(
            "\t".join(
                (
                    domain,
                    include_sub,
                    path,
                    "TRUE" if is_secure else "FALSE",
                    str(expiry),
                    name,
                    value.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r"),
                )
            )
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(out_path, 0o600)  # cookies may contain session tokens
    return 0


def main() -> int:
    home = Path.home()
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/qutebrowser-cookies.txt")
    # qutebrowser's data dir can be overridden via QUTE_WEBENGINE_DATADIR; default is ~/.local/share/qutebrowser.
    profile_dir = Path(os.environ.get("QUTE_WEBENGINE_DATADIR", str(home / ".local" / "share" / "qutebrowser")))
    return convert(profile_dir, out_path)


if __name__ == "__main__":
    sys.exit(main())
