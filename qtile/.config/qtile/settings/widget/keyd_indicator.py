from libqtile import hook
from libqtile.widget import base
from evdev import UInput, ecodes as e
from ..theme import colors as theme
import fnmatch
import subprocess
import sys
import threading
import select
import os
import time

ICON_VIM = "󰰓 "
ICON_VIS = "󰰫 "
ICON_INS = "󰰄 "
VIM_LAYER = "vimmode"
VISUAL_LAYER = "visual"
APP_CONF = os.path.expanduser("~/.config/keyd/app.conf")


def _parse_app_config() -> list[str]:
    """Read app.conf and return app class patterns that have vimmode bindings.

    Each [class|title] section becomes a class pattern.
    Excludes [*] catch-all (not a real app pattern).
    Returns [] if file is missing or unreadable.
    """
    patterns: list[str] = []
    try:
        for line in open(APP_CONF):
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]
                if "|" in section:
                    section = section.split("|")[0]
                if section and section != "*":
                    patterns.append(section)
    except (FileNotFoundError, PermissionError):
        pass
    return patterns


def _active_layers(initial: str) -> list[str]:
    parts = initial.split("/")[-1].split("+")
    return parts[1:] if len(parts) > 1 else []


class _KeydListener:
    """Reads keyd listen in a daemon thread and calls back on state change."""

    def __init__(self, on_state: callable, on_overlay_change: callable):
        self._on_state = on_state
        self._on_overlay_change = on_overlay_change
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._stop = threading.Event()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    @staticmethod
    def _overlay_procs_active() -> bool:
        """Check if layer-shell overlay processes are running via /proc.

        Reads /proc/{pid}/comm directly — no fork/exec overhead.
        """
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

    def _run(self):
        SCAN_INTERVAL = 0.2  # seconds between /proc scans
        last_scan = 0.0
        overlay_was_active = False
        vim_on = False
        vis_on = False

        while not self._stop.is_set():
            try:
                proc = subprocess.Popen(
                    ["keyd", "listen"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                assert proc.stdout is not None
                poll = select.poll()
                poll.register(proc.stdout, select.POLLIN)

                while not self._stop.is_set():
                    events = poll.poll(500)
                    now = time.monotonic()

                    # Periodic layer-shell overlay scan — piggybacks on
                    # the existing poll timeout, no extra wakeups.
                    if now - last_scan >= SCAN_INTERVAL:
                        last_scan = now
                        active = self._overlay_procs_active()
                        if active != overlay_was_active:
                            overlay_was_active = active
                            self._on_overlay_change(active)

                    if not events:
                        continue
                    line = proc.stdout.readline()
                    if not line:
                        continue
                    line = line.strip()
                    if not line:
                        continue

                    new_vim = vim_on
                    new_vis = vis_on
                    if line.startswith("/"):
                        layers = _active_layers(line)
                        new_vim = VIM_LAYER in layers
                        new_vis = VISUAL_LAYER in layers
                    elif line == f"+{VIM_LAYER}":
                        new_vim = True
                    elif line == f"-{VIM_LAYER}":
                        new_vim = False
                    elif line == f"+{VISUAL_LAYER}":
                        new_vis = True
                    elif line == f"-{VISUAL_LAYER}":
                        new_vis = False
                    else:
                        continue

                    if new_vim != vim_on or new_vis != vis_on:
                        vim_on = new_vim
                        vis_on = new_vis
                        self._on_state(vim_on, vis_on)
                proc.terminate()
            except Exception:
                if not self._stop.is_set():
                    threading.Event().wait(2)


class KeydIndicator(base._TextBox):
    """Qtile bar widget for keyd vimmode indicator.

    Shows vim/insert icon when a vimmode-enabled app is focused.
    Auto-detects apps from ~/.config/keyd/app.conf unless vim_apps is set.
    Auto-toggles vimmode on focus boundary via evdev F24 simulation.
    Background thread watches keyd listen for state changes.
    """

    defaults = [
        (
            "vim_apps",
            None,  # None = auto-detect from app.conf
            "List of WM_CLASS patterns. None = auto-detect from app.conf",
        ),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, "", **config)
        self.add_defaults(KeydIndicator.defaults)
        self._focused_app: str | None = None
        self._external_text = ""
        self._vimmode_active = False
        self._visual_active = False
        self._last_f24_time = 0.0
        self._pre_overlay_vim = False
        self._overlay_process_active = False
        self._ui: UInput | None = None
        self._listener: _KeydListener | None = None

    @property
    def _vim_apps(self) -> list[str]:
        apps = self.vim_apps
        if apps is not None:
            return apps
        return _parse_app_config()

    # ------------------------------------------------------------------
    # Startup / focus hooks
    # ------------------------------------------------------------------

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.client_focus(self._on_focus_change)

        # Sync initial vimmode state once
        self._sync_initial_state()

        # Background listener replaces the old systemd indicator.py service.
        # Also scans /proc for layer-shell overlay processes (rofi, wlr-which-key)
        # at 200ms intervals via the existing poll timeout — zero extra wakeups.
        self._listener = _KeydListener(
            lambda vim, vis: qtile.call_soon_threadsafe(self._apply_state, vim, vis),
            lambda active: qtile.call_soon_threadsafe(self._set_overlay_state, active),
        )
        self._listener.start()

        # Track initial focus
        win = qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class:
                self._focused_app = wm_class[0]
        self._handle_overlay()
        self._update_display()

    def _sync_initial_state(self) -> None:
        try:
            proc = subprocess.run(
                ["timeout", "0.5", "keyd", "listen"],
                capture_output=True, text=True, timeout=1,
            )
            for line in proc.stdout.strip().split("\n"):
                if line.startswith("/"):
                    layers = _active_layers(line)
                    vim = VIM_LAYER in layers
                    vis = VISUAL_LAYER in layers
                    self._vimmode_active = vim
                    self._visual_active = vis
                    if vis:
                        self._external_text = ICON_VIS
                    elif vim:
                        self._external_text = ICON_VIM
                    else:
                        self._external_text = ICON_INS
                    return
        except Exception:
            pass

    def _apply_state(self, vimmode_active: bool, visual_active: bool) -> None:
        """Called from Qtile event loop via call_soon_threadsafe."""
        self._vimmode_active = vimmode_active
        self._visual_active = visual_active

        if visual_active:
            self._external_text = ICON_VIS
        elif vimmode_active:
            self._external_text = ICON_VIM
        else:
            self._external_text = ICON_INS

        # Vimmode turned ON by user (CapsLock) → also send Escape
        # so CapsLock closes menus/dialogs even when mapper doesn't switch.
        # If OUR F24 caused the toggle (within 100ms), skip — auto-toggle
        # shouldn't send spurious Escape events.
        if vimmode_active and (time.time() - self._last_f24_time) > 0.1:
            self._send_escape()

        self._update_display()

    # ------------------------------------------------------------------
    # Overlay detection — rofi / wlr-which-key are pure layer-shell
    # surfaces on Wayland. They don't trigger client_focus or
    # client_managed, so the bg thread scans /proc for these processes
    # at 200ms intervals (piggybacked on the keyd listener poll timeout).
    # Focus-change detection covers the rare case where an overlay is
    # registered as a regular window.
    # ------------------------------------------------------------------

    def _set_overlay_state(self, active: bool) -> None:
        """Called from bg thread via call_soon_threadsafe when /proc scan
        detects a layer-shell overlay process start or exit."""
        self._overlay_process_active = active
        self._handle_overlay()

    def _overlay_active(self) -> bool:
        """Check if an overlay is the current_window (rare — most
        layer-shell surfaces aren't tracked as windows)."""
        rofi_or_which_key = ("rofi", "wlr-which-key")
        win = self.qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class and wm_class[0] in rofi_or_which_key:
                return True
        return False

    def _handle_overlay(self) -> None:
        """Toggle vimmode when a layer-shell overlay appears or disappears.

        Combines two detection sources:
        - bg thread /proc scan (layer-shell surfaces, 200ms granularity)
        - focus change check (overlays registered as regular windows)
        """
        active = self._overlay_process_active or self._overlay_active()
        if active:
            if self._vimmode_active and not self._pre_overlay_vim:
                self._pre_overlay_vim = True
                self._toggle_vimmode()
        else:
            # Only restore if keyd is still in the OFF state we left it.
            # If the user manually toggled vimmode back ON during the
            # overlay (via CapsLock), _vimmode_active is True and
            # we must not toggle again.
            if self._pre_overlay_vim and not self._vimmode_active:
                self._toggle_vimmode()
            self._pre_overlay_vim = False

    # ------------------------------------------------------------------
    # CapsLock-forwarding — send Escape via evdev when user toggles vimmode
    # ------------------------------------------------------------------

    def _send_escape(self) -> None:
        if self._ui is None:
            try:
                self._ui = UInput()
            except Exception:
                return
        try:
            # Send F23 — keyd maps it to ESC via default.conf, then outputs
            # a real Escape to the compositor.  Sending KEY_ESC directly
            # wouldn't work because keyd would re-remap it (esc = capslock).
            self._ui.write(e.EV_KEY, e.KEY_F23, 1)
            self._ui.write(e.EV_KEY, e.KEY_F23, 0)
            self._ui.syn()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Auto-toggle — lazy uinput, static f24 in default.conf
    # ------------------------------------------------------------------

    def _toggle_vimmode(self) -> None:
        self._last_f24_time = time.time()
        if self._ui is None:
            try:
                self._ui = UInput()
            except Exception as ex:
                print(f"[keyd] uinput init failed: {ex}", file=sys.stderr)
                self._last_f24_time = 0.0
                return
        try:
            self._ui.write(e.EV_KEY, e.KEY_F24, 1)
            self._ui.write(e.EV_KEY, e.KEY_F24, 0)
            self._ui.syn()
        except Exception as ex:
            print(f"[keyd] toggle failed: {ex}", file=sys.stderr)
            self._last_f24_time = 0.0

    # ------------------------------------------------------------------
    # Focus tracking
    # ------------------------------------------------------------------

    def _on_focus_change(self, client):
        if client is None:
            self._focused_app = None
        else:
            wm_class = client.get_wm_class()
            self._focused_app = wm_class[0] if wm_class else None
        self._handle_overlay()
        self._update_display()

    def _update_display(self) -> None:
        apps = self._vim_apps
        in_vim_app = self._focused_app is not None and any(
            fnmatch.fnmatch(self._focused_app, p) for p in apps
        )
        if in_vim_app:
            if self._vimmode_active or self._visual_active:
                self.foreground = theme["red"]
            else:
                self.foreground = theme["green"]
        else:
            self.foreground = theme["fg"]
        self.update(self._external_text if in_vim_app else "")

    def finalize(self):
        if self._listener is not None:
            self._listener.stop()
        hook.unsubscribe.client_focus(self._on_focus_change)
        if self._ui is not None:
            try:
                self._ui.close()
            except Exception:
                pass
        base._TextBox.finalize(self)
