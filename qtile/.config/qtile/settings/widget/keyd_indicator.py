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

ICON_VIM = "󰰓 "
ICON_INS = "󰰄 "
VIM_LAYER = "vimmode"
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

    def __init__(self, on_state: callable):
        self._on_state = on_state
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._stop = threading.Event()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _run(self):
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
                    if not events:
                        continue
                    line = proc.stdout.readline()
                    if not line:
                        continue
                    line = line.strip()
                    if not line:
                        continue

                    vim_on: bool | None = None
                    if line.startswith("/"):
                        layers = _active_layers(line)
                        vim_on = VIM_LAYER in layers
                    elif line == f"+{VIM_LAYER}":
                        vim_on = True
                    elif line == f"-{VIM_LAYER}":
                        vim_on = False

                    if vim_on is not None:
                        self._on_state(ICON_VIM if vim_on else ICON_INS)
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
        self._ui: UInput | None = None
        self._listener: _KeydListener | None = None
        self._health_handle: object | None = None

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

        # Background listener replaces the old systemd indicator.py service
        self._listener = _KeydListener(
            lambda text: qtile.call_soon_threadsafe(self._apply_state, text)
        )
        self._listener.start()

        # Track initial focus
        win = qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class:
                self._focused_app = wm_class[0]
                self._update_display()

        # Periodic safety check: catch layer-shell overlays (rofi, wlr-which-key)
        # that neither the mapper nor client_focus detects.
        self._schedule_health_check()

    def _sync_initial_state(self) -> None:
        try:
            proc = subprocess.run(
                ["timeout", "0.5", "keyd", "listen"],
                capture_output=True, text=True, timeout=1,
            )
            for line in proc.stdout.strip().split("\n"):
                if line.startswith("/"):
                    layers = _active_layers(line)
                    self._external_text = ICON_VIM if VIM_LAYER in layers else ICON_INS
                    return
        except Exception:
            pass

    def _apply_state(self, text: str) -> None:
        """Called from Qtile event loop via call_soon_threadsafe."""
        self._external_text = text
        self._update_display()

    # ------------------------------------------------------------------
    # Safety check — catches layer-shell overlays (rofi, wlr-which-key)
    # that bypass both the wlr_foreign_toplevel mapper and client_focus.
    # ------------------------------------------------------------------

    def _schedule_health_check(self) -> None:
        loop = getattr(self.qtile, "_eventloop", None)
        if loop is not None:
            self._health_handle = loop.call_later(1, self._health_check)

    def _health_check(self) -> None:
        """If vimmode is ON but current app is not a vim-app, toggle OFF.

        Layer-shell overlays (rofi, wlr-which-key) don't trigger
        client_focus and the mapper can't see them, so old vim bindings
        persist. This catches it within ~1s.
        """
        if self._external_text != ICON_VIM:
            self._schedule_health_check()
            return

        win = self.qtile.current_window
        if win is None:
            self._schedule_health_check()
            return
        wm_class = win.get_wm_class()
        current_app = wm_class[0] if wm_class else None
        in_vim = current_app is not None and any(
            fnmatch.fnmatch(current_app, p) for p in self._vim_apps
        )
        if not in_vim:
            print("[keyd] health: vimmode ON outside vim-app -> toggle OFF", file=sys.stderr)
            self._toggle_vimmode()
        self._schedule_health_check()

    # ------------------------------------------------------------------
    # Auto-toggle — lazy uinput, static f24 in default.conf
    # ------------------------------------------------------------------

    def _toggle_vimmode(self) -> None:
        if self._ui is None:
            try:
                self._ui = UInput()
            except Exception as ex:
                print(f"[keyd] uinput init failed: {ex}", file=sys.stderr)
                return
        try:
            self._ui.write(e.EV_KEY, e.KEY_F24, 1)
            self._ui.write(e.EV_KEY, e.KEY_F24, 0)
            self._ui.syn()
        except Exception as ex:
            print(f"[keyd] toggle failed: {ex}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Focus tracking
    # ------------------------------------------------------------------

    def _on_focus_change(self, client):
        old_app = self._focused_app

        if client is None:
            self._focused_app = None
        else:
            wm_class = client.get_wm_class()
            self._focused_app = wm_class[0] if wm_class else None

        apps = self._vim_apps
        was_in = old_app is not None and any(
            fnmatch.fnmatch(old_app, p) for p in apps
        )
        now_in = self._focused_app is not None and any(
            fnmatch.fnmatch(self._focused_app, p) for p in apps
        )

        if now_in and not was_in:
            if self._external_text == ICON_INS or self._external_text == "":
                print("[keyd] enter vim-app -> toggle ON", file=sys.stderr)
                self._toggle_vimmode()
        elif was_in and not now_in:
            if self._external_text == ICON_VIM:
                print("[keyd] leave vim-app -> toggle OFF", file=sys.stderr)
                self._toggle_vimmode()
            else:
                print("[keyd] leave vim-app (was OFF) -> skip", file=sys.stderr)

        self._update_display()

    def _update_display(self) -> None:
        apps = self._vim_apps
        in_vim_app = self._focused_app is not None and any(
            fnmatch.fnmatch(self._focused_app, p) for p in apps
        )
        if in_vim_app:
            self.foreground = theme["red"] if self._external_text == ICON_VIM else theme["green"]
        else:
            self.foreground = theme["fg"]
        self.update(self._external_text if in_vim_app else "")

    def finalize(self):
        if self._listener is not None:
            self._listener.stop()
        if self._health_handle is not None:
            try:
                self._health_handle.cancel()
            except Exception:
                pass
        hook.unsubscribe.client_focus(self._on_focus_change)
        if self._ui is not None:
            try:
                self._ui.close()
            except Exception:
                pass
        base._TextBox.finalize(self)
