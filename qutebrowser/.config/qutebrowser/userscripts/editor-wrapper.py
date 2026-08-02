#!/usr/bin/env python3
"""qutebrowser editor wrapper.

Strips trailing newline from edited text before qutebrowser reads it back.
Usage: c.editor.command = ["...editor-wrapper.py", "{file}", "{line}", "{column}"]
"""

import subprocess
import sys

file_path = sys.argv[1]
line = sys.argv[2] if len(sys.argv) > 2 else "1"
column = sys.argv[3] if len(sys.argv) > 3 else "0"

subprocess.run(
    [
        "kitty",
        "--single-instance",
        "--app-id",
        "kitty-float",
        "nvim",
        file_path,
        "+set ft=markdown",
        "+startinsert",
        f"+call cursor({line}, {column})",
    ]
)

with open(file_path) as f:
    content = f.read()
if content.endswith("\n"):
    with open(file_path, "w") as f:
        f.write(content.rstrip("\n"))
