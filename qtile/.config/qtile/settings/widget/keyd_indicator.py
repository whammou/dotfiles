from libqtile import hook
from libqtile.widget import base
from ..theme import colors as theme
import fnmatch
import json
import os
import subprocess
import sys

ICON_VIM = "󰰓 "
ICON_VIS = "󰰫 "
ICON_INS = "󰰄 "

APP_CONF = os.path.expanduser("~/.config/keyd/app.conf")
_SCRIPT = os.path.join(os.path.dirname(__file__), "keyd_monitor.py")


def _parse_app_config() -> list[str]:
    """Read app.conf and return app class patterns that have vimmode bindings."""
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


class KeydIndicator(base._TextBox):
    """Qtile bar widget for keyd vimmode indicator.

    Spawns ``keyd_monitor.py`` as a background subprocess and reads
    JSON state lines from its stdout.  Pure display — no knowledge of
    keyd IPC, /proc scanning, or uinput.
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
        self._external_text = ""
        self._mode = "insert"  # "vim" | "visual" | "insert"
        self._overlay_on = False
        self._proc: subprocess.Popen | None = None
        self._buf = ""
        self._loop = None
        self._finalized = False

    @property
    def _vim_apps(self) -> list[str]:
        apps = self.vim_apps
        if apps is not None:
            return apps
        return _parse_app_config()

    def _is_vim_app_focused(self) -> bool:
        apps = self._vim_apps
        return self._focused_app is not None and any(
            fnmatch.fnmatch(self._focused_app, p) for p in apps
        )

    # ------------------------------------------------------------------
    # Subprocess lifecycle
    # ------------------------------------------------------------------

    def _spawn_monitor(self) -> bool:
        """Start (or restart) the keyd_monitor.py subprocess."""
        if self._proc is not None:
            try:
                self._proc.terminate()
                self._proc.wait(2)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None

        try:
            self._proc = subprocess.Popen(
                [sys.executable, _SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            assert self._proc.stdout is not None
            os.set_blocking(self._proc.stdout.fileno(), False)
            if self._loop is not None:
                self._loop.add_reader(self._proc.stdout.fileno(), self._on_stdout_data)
            return True
        except Exception as ex:
            print(f"[keyd] spawn failed: {ex}", file=sys.stderr)
            self._proc = None
            return False

    def _kill_monitor(self) -> None:
        if self._proc is None:
            return
        try:
            if self._loop is not None and self._proc.stdout is not None:
                self._loop.remove_reader(self._proc.stdout.fileno())
        except Exception:
            pass
        try:
            self._proc.terminate()
            self._proc.wait(2)
        except Exception:
            try:
                self._proc.kill()
            except Exception:
                pass
        self._proc = None
        self._buf = ""

    # ------------------------------------------------------------------
    # stdout reader — event-driven
    # ------------------------------------------------------------------

    def _on_stdout_data(self) -> None:
        """Event-loop callback: subprocess stdout has data."""
        if self._proc is None or self._proc.stdout is None:
            return
        try:
            raw = os.read(self._proc.stdout.fileno(), 65536)
            if not raw:
                self._on_monitor_died()
                return
            self._buf += raw.decode("utf-8", errors="replace")
            while "\n" in self._buf:
                line, self._buf = self._buf.split("\n", 1)
                line = line.strip()
                if line:
                    try:
                        state = json.loads(line)
                        self._apply_state(
                            state.get("mode", "insert"),
                            state.get("overlay", False),
                        )
                    except json.JSONDecodeError:
                        pass
        except (BlockingIOError, OSError, ValueError):
            self._on_monitor_died()

    def _on_monitor_died(self) -> None:
        """Monitor process died — clean up and restart after a delay."""
        self._kill_monitor()
        if self._loop is not None and not self._finalized:
            self._loop.call_later(2.0, self._spawn_monitor)

    # ------------------------------------------------------------------
    # State application (called from event loop)
    # ------------------------------------------------------------------

    def _apply_state(self, mode: str, overlay: bool) -> None:
        self._mode = mode
        self._overlay_on = overlay
        self._update_display()

    # ------------------------------------------------------------------
    # Startup / focus hooks
    # ------------------------------------------------------------------

    def _configure(self, qtile, bar):
        try:
            self._configure_impl(qtile, bar)
        except Exception:
            import traceback

            traceback.print_exc()

    def _configure_impl(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        self._loop = qtile._eventloop
        hook.subscribe.client_focus(self._on_focus_change)

        # Spawn the background monitor
        self._spawn_monitor()

        # Track initial focus
        win = qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class:
                self._focused_app = wm_class[0]
        self._update_display()

    # ------------------------------------------------------------------
    # Display update
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        in_vim_app = self._is_vim_app_focused()
        if in_vim_app:
            if self._mode == "visual":
                self._external_text = ICON_VIS
                self.foreground = theme["red"]
            elif self._mode == "vim":
                self._external_text = ICON_VIM
                self.foreground = theme["red"]
            else:
                self._external_text = ICON_INS
                self.foreground = theme["green"]
        else:
            self.foreground = theme["fg"]
        self.update(self._external_text if in_vim_app else "")

    # ------------------------------------------------------------------
    # Focus tracking — pure display, no uinput
    # ------------------------------------------------------------------

    def _on_focus_change(self, client):
        if client is None:
            self._focused_app = None
        else:
            wm_class = client.get_wm_class()
            self._focused_app = wm_class[0] if wm_class else None
        self._update_display()

    # ------------------------------------------------------------------

    def finalize(self):
        self._finalized = True
        self._kill_monitor()
        hook.unsubscribe.client_focus(self._on_focus_change)
        base._TextBox.finalize(self)
