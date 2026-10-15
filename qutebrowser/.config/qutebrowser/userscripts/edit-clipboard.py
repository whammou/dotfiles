#!/usr/bin/env python3
"""External editor fallback for qutebrowser issue #2215.

For contenteditable/CodeMirror/Quill fields where `:edit-text` silently
does nothing: opens an empty buffer in nvim and live-syncs every save
into the field via `document.execCommand('insertText')` — the same
trusted-input path real typing takes, so React/CodeMirror/Quill fire
input events. Existing field text is intentionally not captured.

Buffer semantics per save: unwritten file does nothing; an explicitly
saved empty buffer clears the field (undoable in-field with Ctrl-Z);
anything else replaces the field.

Usage: :spawn --userscript edit-clipboard.py  (Ctrl-e insert / Ctrl-i normal)
Requires: kitty, nvim.
"""

import json
import os
import subprocess
import sys
import tempfile
import time


def qute_cmd(fifo: str, cmd: str) -> None:
    with open(fifo, "a") as f:
        f.write(cmd + "\n")


def wake(fifo: str) -> None:
    # tabfreeze suspends unfocused tabs (Frozen renderer drops input and
    # JS); wake the current tab before touching the field. No-op when
    # tabfreeze is not armed.
    qute_cmd(fifo, "tabfreeze-wake")


def pin(fifo: str) -> None:
    qute_cmd(fifo, "jseval --quiet "
                   "window._quteEditEl = document.activeElement; "
                   "try{window._quteEditEl.focus();}catch(e){}")


_DEEP_JS = ("function deep(el){try{var g=0;while(el&&g<5){g++;var n=null;"
             "try{if(el.contentDocument&&el.contentDocument.activeElement)"
             "n=el.contentDocument.activeElement;}catch(e){}"
             "try{if(!n&&el.shadowRoot&&el.shadowRoot.activeElement)"
             "n=el.shadowRoot.activeElement;}catch(e){}"
             "if(!n||n===el)break;el=n;}}catch(e){}return el;}")


_SELECT_JS = ("try{if(el&&(el.tagName==='INPUT'||el.tagName==='TEXTAREA'))"
               "{el.select();}else{var _s=(el&&el.ownerDocument||document)"
               ".getSelection();if(el){_s.selectAllChildren(el);}}}"
               "catch(e){}")


def js_insert_command(text: str) -> str:
    # json.dumps is always a valid JS string literal without raw newlines,
    # and :jseval takes the whole remainder of the line (maxsplit=0), so
    # arbitrary edited text survives intact on one FIFO line.
    payload = json.dumps(text, ensure_ascii=True)
    return ("jseval --quiet (function(){" + _DEEP_JS +
            "var el=deep((window._quteEditEl&&window._quteEditEl.isConnected)"
            "?window._quteEditEl:document.activeElement);"
            "var doc=(el&&el.ownerDocument)||document;"
            "try{el.focus();}catch(e){}"
            "try{" + _SELECT_JS + ";}catch(e){}"
            f"try{{doc.execCommand('insertText',false,{payload});}}"
            "catch(e){}"
             "})()")


def maybe_paste(fifo: str, tmp: str, last_sent: bytes | None) -> bytes | None:
    # Paste the file if it changed since the last paste. Returns the
    # content marker to compare against next time.
    try:
        with open(tmp, "rb") as f:
            raw = f.read()
    except OSError:
        return last_sent
    if len(raw) == 0:
        # Never saved: nothing to do.
        return raw
    if raw == last_sent:
        return last_sent
    # nvim terminates the file with a newline; strip it so it doesn't
    # land in the field. An explicitly saved empty buffer clears it.
    edited = raw.decode("utf-8", "replace").rstrip("\n")
    # The tab may have refrozen while editing; re-wake it first. The
    # evals that follow run in order on the same channel: pin, then
    # insert.
    wake(fifo)
    pin(fifo)
    qute_cmd(fifo, js_insert_command(edited))
    return raw


def main() -> int:
    fifo = os.environ.get("QUTE_FIFO")
    if not fifo:
        print("edit-clipboard: QUTE_FIFO not set (run via :spawn --userscript)",
              file=sys.stderr)
        return 1

    fd, tmp = tempfile.mkstemp(prefix="qute-edit-", suffix=".md")
    try:
        os.close(fd)
        proc = subprocess.Popen(
            [
                "kitty", "--single-instance", "--app-id", "qutebrowser-editor",
                "nvim", tmp, "+set ft=markdown", "+startinsert",
            ],
        )
        last_mtime: int | None = None
        last_sent: bytes | None = None
        while proc.poll() is None:
            try:
                mtime = os.stat(tmp).st_mtime_ns
            except OSError:
                mtime = None
            if mtime != last_mtime:
                last_mtime = mtime
                # Let the write settle so a partial save is never pasted.
                time.sleep(0.3)
                last_sent = maybe_paste(fifo, tmp, last_sent)
            else:
                time.sleep(0.2)
        # Final flush: catches a save that landed with the quit.
        maybe_paste(fifo, tmp, last_sent)
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
