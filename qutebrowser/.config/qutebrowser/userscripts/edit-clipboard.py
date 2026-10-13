#!/usr/bin/env python3
"""Clipboard fallback editor for qutebrowser issue #2215.

For contenteditable/CodeMirror/Quill fields where `:edit-text` silently
does nothing (setting `.value` is a no-op on divs), this copies via the
page's own copy handling, edits in nvim, and pastes back through a real
paste keypress so framework input events fire.

Usage: :spawn --userscript edit-clipboard.py  (bound to <Alt-e> in insert mode)
Requires: wl-copy, wl-paste (Wayland), kitty, nvim.
"""

import os
import subprocess
import sys
import tempfile
import time

COPY_WAIT = 0.4
PASTE_WAIT = 0.2
TIMEOUT = 10


def qute_cmd(fifo: str, cmd: str) -> None:
    with open(fifo, "a") as f:
        f.write(cmd + "\n")


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, timeout=TIMEOUT, check=False, **kwargs)


def wl_paste_plain() -> tuple[str, bool]:
    # Returns (text, clipboard_owned). Explicit text/plain selection matters:
    # rich editors (ProseMirror/TipTap) offer text/html first and bare
    # wl-paste infers it, yielding markup like <p data-pm-slice="...">.
    types_proc = run(["wl-paste", "--list-types"], capture_output=True, text=True)
    if types_proc.returncode != 0:
        return "", False
    types = types_proc.stdout.split()
    plain = next((t for t in types if t == "text/plain"), None)
    if plain is None:
        plain = next((t for t in types if t.startswith("text/plain")), None)
    if plain is None:
        return "", True
    proc = run(["wl-paste", "--no-newline", "--type", plain],
               capture_output=True, text=True)
    if proc.returncode != 0:
        return "", True
    return proc.stdout, True


def main() -> int:
    fifo = os.environ.get("QUTE_FIFO")
    if not fifo:
        print("edit-clipboard: QUTE_FIFO not set (run via :spawn --userscript)",
              file=sys.stderr)
        return 1

    # QUTE_SELECTED_TEXT is inline text; QUTE_TEXT is a *path* to a tempfile
    # holding the whole page plaintext (never the field) — so ignore it.
    seed = os.environ.get("QUTE_SELECTED_TEXT") or ""

    if seed:
        content = seed
        blank = False
    else:
        # Seed a sentinel so "copy produced nothing" is distinguishable from
        # real clipboard failure: an empty field copies nothing, leaving the
        # sentinel (or no owner); a working copy overwrites it. Seeding also
        # buries any stale clipboard content.
        token = f"qute-edit-blank-{os.getpid()}-{time.time_ns()}"
        run(["wl-copy"], input=token, text=True)
        # Copy via the page's own handler — CodeMirror/Quill implement copy,
        # so Ctrl-A/Ctrl-C works where JS `.value` reads fail.
        qute_cmd(fifo, "fake-key <Ctrl-a> ;; fake-key <Ctrl-c>")
        time.sleep(COPY_WAIT)
        content, have_clip = wl_paste_plain()
        if not have_clip:
            qute_cmd(fifo, "message-error 'edit-clipboard: clipboard unavailable'")
            return 1
        # Empty plain text, missing text/plain, or surviving sentinel all mean
        # the field contributed nothing: open a blank buffer for composing.
        # (An uncopyable widget lands here too — pasted append-only below,
        # so existing content is never wiped.)
        blank = not content or content == token
        if blank:
            content = ""

    fd, tmp = tempfile.mkstemp(prefix="qute-edit-", suffix=".md")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)

        subprocess.run(
            [
                "kitty", "--single-instance", "--app-id", "qutebrowser-editor",
                "nvim", tmp, "+set ft=markdown", "+startinsert",
            ],
            check=False,
        )

        with open(tmp) as f:
            edited = f.read()
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass

    if edited == content:
        return 0

    # wl-copy daemonizes and holds the clipboard for the paste below.
    proc = run(["wl-copy"], input=edited, text=True)
    if proc.returncode != 0:
        qute_cmd(fifo, "message-error 'edit-clipboard: wl-copy failed'")
        return 1
    time.sleep(PASTE_WAIT)

    # Real paste path fires input events React/CodeMirror/Quill listen for,
    # unlike JS `.value = ...` assignment. Blank-origin paste skips select-all
    # so a misdetected non-empty field gets appended to, never wiped.
    if blank:
        qute_cmd(fifo, "fake-key <Ctrl-v>")
    else:
        qute_cmd(fifo, "fake-key <Ctrl-a> ;; fake-key <Ctrl-v>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
