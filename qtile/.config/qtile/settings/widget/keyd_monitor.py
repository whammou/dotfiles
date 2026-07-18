#!/usr/bin/env python3
"""Background monitor for keyd vimmode state.

Connects to keyd daemon via /run/keyd.socket, subscribes to layer-state
changes, monitors /proc for layer-shell overlays (rofi, wlr-which-key),
and manages uinput for automatic vimmode toggles.

Outputs one state line per change to stdout for the Qtile widget to
consume.  Runs until stdin closes or SIGTERM.
"""

import json
import os
import select
import socket
import struct
import sys
import time

SOCKET_PATH = "/run/keyd.socket"
IPC_LAYER_LISTEN = 6
VIM_LAYER = "vimmode"
VISUAL_LAYER = "visual"
SCAN_INTERVAL = 0.2

# ---------------------------------------------------------------------------
# keyd IPC helpers
# ---------------------------------------------------------------------------

def _subscribe_msg() -> bytes:
    """4112-byte IPC_LAYER_LISTEN subscribe message."""
    return (
        struct.pack("<ii", IPC_LAYER_LISTEN, 0)
        + b"\x00" * 4096
        + struct.pack("<Q", 0)
    )


def _active_layers(line: str) -> list[str]:
    parts = line.split("/")[-1].split("+")
    return parts[1:] if len(parts) > 1 else []


# ---------------------------------------------------------------------------
# Overlay /proc scan
# ---------------------------------------------------------------------------

def _overlay_procs_active() -> bool:
    targets = frozenset(("rofi", "wlr-which-key"))
    try:
        for entry in os.listdir("/proc"):
            if entry.isdigit():
                try:
                    with open(f"/proc/{entry}/comm") as f:
                        if f.read().strip() in targets:
                            return True
                except OSError:
                    pass
    except OSError:
        pass
    return False


# ---------------------------------------------------------------------------
# uinput wrappers (lazy)
# ---------------------------------------------------------------------------

_ui = None  # UInput instance, created on first use


def _ensure_ui():
    global _ui
    if _ui is not None:
        return _ui
    try:
        from evdev import UInput, ecodes as e
        _ui = UInput()
        return _ui
    except Exception as ex:
        print(f"[keyd-mon] uinput init failed: {ex}", file=sys.stderr)
        return None


def _close_ui():
    global _ui
    if _ui is not None:
        try:
            _ui.close()
        except Exception:
            pass
        _ui = None


def send_escape():
    """Send F23 — keyd maps it to ESC via default.conf."""
    ui = _ensure_ui()
    if ui is None:
        return
    try:
        from evdev import ecodes as e
        ui.write(e.EV_KEY, e.KEY_F23, 1)
        ui.write(e.EV_KEY, e.KEY_F23, 0)
        ui.syn()
    except Exception as ex:
        print(f"[keyd-mon] send_escape failed: {ex}", file=sys.stderr)


def toggle_vimmode():
    """Send F24 — keyd toggles vimmode via app.conf."""
    global _last_toggle
    ui = _ensure_ui()
    if ui is None:
        return
    try:
        from evdev import ecodes as e
        ui.write(e.EV_KEY, e.KEY_F24, 1)
        ui.write(e.EV_KEY, e.KEY_F24, 0)
        ui.syn()
        _last_toggle = time.time()
    except Exception as ex:
        print(f"[keyd-mon] toggle failed: {ex}", file=sys.stderr)


# ---------------------------------------------------------------------------
# IPC with Qtile widget
# ---------------------------------------------------------------------------

def send_state(mode: str, overlay: bool) -> None:
    """Write a state line to stdout for the widget to consume.

    Format: JSON with fields ``mode`` and ``overlay``.
    """
    line = json.dumps(
        {"mode": mode, "overlay": overlay},
        separators=(",", ":"),
    )
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Line parser — returns (changed, new_vim, new_vis) or None for unknown lines
# ---------------------------------------------------------------------------

def parse_keyd_line(
    line: str, vim_on: bool, vis_on: bool
) -> tuple[bool, bool, bool] | None:
    """Parse a single keyd listen line and return (changed, vim, vis).

    Returns None for unrecognised lines.
    """
    if line.startswith("/"):
        layers = _active_layers(line)
        nv = VIM_LAYER in layers
        nvs = VISUAL_LAYER in layers
        return (nv != vim_on or nvs != vis_on), nv, nvs
    elif line == f"+{VIM_LAYER}":
        return (not vim_on), True, vis_on
    elif line == f"-{VIM_LAYER}":
        return vim_on, False, vis_on
    elif line == f"+{VISUAL_LAYER}":
        return (not vis_on), vim_on, True
    elif line == f"-{VISUAL_LAYER}":
        return vis_on, vim_on, False
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # ---- connect to keyd ----
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect(SOCKET_PATH)
        sock.sendall(_subscribe_msg())
    except Exception as ex:
        print(f"[keyd-mon] connect failed: {ex}", file=sys.stderr)
        sys.exit(1)

    # ---- initial state: blocking read ----
    buf = b""
    try:
        sock.settimeout(0.5)
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass

    sock.setblocking(False)
    poll = select.poll()
    poll.register(sock, select.POLLIN)

    vim_on = False
    vis_on = False
    overlay_active = _overlay_procs_active()
    overlay_was = overlay_active
    pre_overlay_vim = False
    last_scan = 0.0
    global _last_toggle
    _last_toggle = 0.0

    def current_mode() -> str:
        return "visual" if vis_on else ("vim" if vim_on else "insert")

    # Process initial buffer
    while b"\n" in buf:
        line_bytes, buf = buf.split(b"\n", 1)
        line_str = line_bytes.decode("utf-8", errors="replace").strip()
        if not line_str:
            continue
        result = parse_keyd_line(line_str, vim_on, vis_on)
        if result is not None:
            _, vim_on, vis_on = result

    send_state(current_mode(), overlay_active)

    # ---- event loop ----
    # Use poll.poll(SCAN_INTERVAL_s) for the keyd socket and piggyback
    # the /proc scan on the same timeout — just like the original approach.

    while True:
        now = time.monotonic()

        # /proc overlay scan — only when a vim-app might be focused
        # (we can't know for sure since we're a separate process, so
        #  we run continuously at a moderate rate)
        if now - last_scan >= SCAN_INTERVAL:
            last_scan = now
            try:
                active = _overlay_procs_active()
                if active != overlay_was:
                    overlay_was = active
                    overlay_active = active
                    send_state(current_mode(), overlay_active)

                    # Overlay appeared → disable vimmode
                    if active:
                        pre_overlay_vim = vim_on
                        if vim_on:
                            toggle_vimmode()
                    # Overlay disappeared → restore vimmode
                    else:
                        if pre_overlay_vim and not vim_on:
                            toggle_vimmode()
                        pre_overlay_vim = False
            except Exception as ex:
                print(f"[keyd-mon] scan error: {ex}", file=sys.stderr)

        # Wait for keyd data (timeout = remaining scan interval)
        timeout_ms = max(50, int((last_scan + SCAN_INTERVAL - time.monotonic()) * 1000))
        events = poll.poll(timeout_ms)
        if not events:
            continue

        try:
            data = sock.recv(4096)
            if not data:
                break  # EOF — keyd daemon disconnected
            buf = data
            while b"\n" in buf:
                line_bytes, buf = buf.split(b"\n", 1)
                line_str = line_bytes.decode("utf-8", errors="replace").strip()
                if not line_str:
                    continue

                result = parse_keyd_line(line_str, vim_on, vis_on)
                if result is None:
                    continue
                changed, vim_on, vis_on = result

                if changed:
                    send_state(current_mode(), overlay_active)

                    # Vim turned ON by user → send Escape (F23)
                    # Skip if our own toggle triggered this within 100 ms.
                    if vim_on and (time.time() - _last_toggle) > 0.1:
                        send_escape()
        except (BlockingIOError, OSError):
            break

    sock.close()
    _close_ui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(f"[keyd-mon] fatal: {ex}", file=sys.stderr)
        sys.exit(1)
