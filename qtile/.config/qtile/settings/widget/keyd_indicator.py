from libqtile import hook
from libqtile.widget import base
from evdev import UInput, ecodes as e
from ..theme import colors as theme
import asyncio
import fnmatch
import os
import sys
import time

ICON_VIM = "󰰓 "
ICON_VIS = "󰰫 "
ICON_INS = "󰰄 "
VIM_LAYER = "vimmode"
VISUAL_LAYER = "visual"
APP_CONF = os.path.expanduser("~/.config/keyd/app.conf")
OVERLAY_APPS = frozenset(("rofi", "wlr-which-key"))


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





class KeydIndicator(base._TextBox):
    """Qtile bar widget for keyd vimmode indicator.

    Shows vim/insert icon when a vimmode-enabled app is focused.
    Auto-detects apps from ~/.config/keyd/app.conf unless vim_apps is set.
    Auto-toggles vimmode on focus boundary via evdev F24 simulation.
    Event-driven: async subprocess reader for keyd listen; hooks for
    layer-shell overlay detection (client_new/client_killed).
    """

    defaults = [
        (
            "vim_apps",
            None,
            "List of WM_CLASS patterns. None = auto-detect from app.conf",
        ),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, "", **config)
        self.add_defaults(KeydIndicator.defaults)
        self._focused_app: str | None = None
        self._external_text = ICON_INS
        self._vimmode_active = False
        self._visual_active = False
        self._last_f24_time = 0.0
        self._pre_overlay_vim = False
        self._overlay_process_active = False
        self._overlay_clients: set[int] = set()
        self._ui: UInput | None = None
        self._keyd_task: asyncio.Task | None = None

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
        hook.subscribe.client_new(self._on_client_new)
        hook.subscribe.client_killed(self._on_client_killed)

        # Event-driven keyd listener via asyncio subprocess
        self._keyd_task = asyncio.ensure_future(self._keyd_listener())

        # Track initial focus
        win = qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class:
                self._focused_app = wm_class[0]
        self._handle_overlay()
        self._update_display()

    async def _keyd_listener(self):
        """Async subprocess reader for `keyd listen` — no polling, no thread."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "keyd", "listen",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            assert proc.stdout is not None

            while True:
                line_bytes = await proc.stdout.readline()
                if not line_bytes:
                    break
                self._process_keyd_line(line_bytes.decode().strip())
        except (OSError, asyncio.CancelledError):
            pass
        except Exception:
            if self._keyd_task is not None and not self._keyd_task.done():
                await asyncio.sleep(2)

    def _process_keyd_line(self, line: str) -> None:
        """Parse a single keyd listen line and update state."""
        if not line:
            return

        new_vim = self._vimmode_active
        new_vis = self._visual_active

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
            return

        if new_vim != self._vimmode_active or new_vis != self._visual_active:
            self._vimmode_active = new_vim
            self._visual_active = new_vis
            self._on_state_changed()

    def _on_state_changed(self) -> None:
        """State from keyd changed — update display and send Escape if needed."""
        if self._visual_active:
            self._external_text = ICON_VIS
        elif self._vimmode_active:
            self._external_text = ICON_VIM
        else:
            self._external_text = ICON_INS

        if self._vimmode_active and (time.time() - self._last_f24_time) > 0.1:
            self._send_escape()

        self._update_display()

    # ------------------------------------------------------------------
    # Overlay detection — event-driven via client_new/client_killed hooks.
    # Wayland layer-shell surfaces (rofi, wlr-which-key) don't trigger
    # client_focus but DO fire client_new when the backend calls
    # qtile.manage() for new LayerStatic surfaces.
    # ------------------------------------------------------------------

    @staticmethod
    def _get_app_id(client) -> str | None:
        """Extract app_id (Wayland) or wm_class (X11) from a client."""
        app_id = getattr(client, "app_id", None)
        if app_id:
            return app_id
        try:
            wm_class = client.get_wm_class()
            return wm_class[0] if wm_class else None
        except Exception:
            return None

    def _on_client_new(self, client):
        app_id = self._get_app_id(client)
        if app_id in OVERLAY_APPS:
            self._overlay_clients.add(id(client))
            if not self._overlay_process_active:
                self._overlay_process_active = True
                self._handle_overlay()

    def _on_client_killed(self, client):
        if id(client) in self._overlay_clients:
            self._overlay_clients.discard(id(client))
            if not self._overlay_clients:
                self._overlay_process_active = False
                self._handle_overlay()

    def _overlay_window_active(self) -> bool:
        """Fallback: check if an overlay is the current_window."""
        win = self.qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class and wm_class[0] in OVERLAY_APPS:
                return True
        return False

    def _handle_overlay(self) -> None:
        """Toggle vimmode when a layer-shell overlay appears or disappears."""
        active = self._overlay_process_active or self._overlay_window_active()
        if active:
            if self._vimmode_active and not self._pre_overlay_vim:
                self._pre_overlay_vim = True
                self._toggle_vimmode()
        else:
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
        if self._keyd_task is not None:
            self._keyd_task.cancel()
        hook.unsubscribe.client_focus(self._on_focus_change)
        hook.unsubscribe.client_new(self._on_client_new)
        hook.unsubscribe.client_killed(self._on_client_killed)
        if self._ui is not None:
            try:
                self._ui.close()
            except Exception:
                pass
        base._TextBox.finalize(self)
