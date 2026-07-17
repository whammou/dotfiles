#!/usr/bin/env python3
"""Watch keyd layer state and push vim-mode indicator to Qtile bar widget.

vimmode ON  -> Vim icon  (global vim navigation)
vimmode OFF -> Pencil icon (normal typing/insert)
unknown     -> empty
"""

import subprocess
import sys
import select
import time

QTILE_WIDGET = "keyd"
QTILE_CMD = "set_state"  # @expose_command() on KeydIndicator.set_state
VIM_LAYER = "vimmode"
ICON_VIM = "󰰓 "
ICON_INS = "󰰄 "
ICON_NONE = ""


def set_qtile(text: str) -> None:
    try:
        subprocess.run(
            [
                "qtile", "cmd-obj", "-o", "widget",
                QTILE_WIDGET, "-f", QTILE_CMD, "-a", text,
            ],
            capture_output=True,
            timeout=3,
        )
    except Exception:
        pass


def active_layers(initial: str) -> list[str]:
    parts = initial.split("/")[-1].split("+")
    return parts[1:] if len(parts) > 1 else []


def main() -> None:
    proc = subprocess.Popen(
        ["keyd", "listen"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    assert proc.stdout is not None
    poll = select.poll()
    poll.register(proc.stdout, select.POLLIN)

    vim_on = False
    had_initial = False

    try:
        while True:
            if proc.poll() is not None:
                time.sleep(2)
                try:
                    poll.unregister(proc.stdout)
                except KeyError:
                    pass
                proc.stdout.close()
                proc.wait()
                proc = subprocess.Popen(
                    ["keyd", "listen"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                assert proc.stdout is not None
                poll.register(proc.stdout, select.POLLIN)
                continue

            events = poll.poll(500)

            if events:
                line = proc.stdout.readline()
                if not line:
                    continue
                line = line.strip()
                if not line:
                    continue

                if line.startswith("/"):
                    layers = active_layers(line)
                    vim_on = VIM_LAYER in layers
                    had_initial = True
                    set_qtile(ICON_VIM if vim_on else ICON_INS)
                    print(
                        f"state: {line} -> {'VIM' if vim_on else 'INS'}",
                        file=sys.stderr,
                    )
                elif line == f"+{VIM_LAYER}":
                    vim_on = True
                    set_qtile(ICON_VIM)
                    print("+vimmode -> VIM", file=sys.stderr)
                elif line == f"-{VIM_LAYER}":
                    vim_on = False
                    set_qtile(ICON_INS)
                    print("-vimmode -> INS", file=sys.stderr)
                elif line.startswith("+") or line.startswith("-"):
                    pass
            elif not had_initial:
                set_qtile(ICON_NONE)
    finally:
        proc.terminate()


if __name__ == "__main__":
    main()
