from libqtile import hook
from libqtile.widget import base
from ..theme import colors as theme
import fnmatch
import os
import select
import subprocess
import sys

ICON_VIM = "󰰓 "
ICON_VIS = "󰰫 "
ICON_INS = "󰰄 "

APP_CONF = os.path.expanduser("~/.config/keyd/app.conf")


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

    Spawns ``keyd listen`` as a background subprocess and parses
    layer state changes from its output.  No daemon, no uinput, no /proc.
    """

    def _vimmode_init(self):
        self._loop = None
        self._finalized = False
        self._focused_app: str | None = None
        self._external_text = ""
        self._vim_on = False
        self._vis_on = False
        self._proc: subprocess.Popen | None = None
        self._buf = ""

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
        self._vimmode_init()

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

    @property
    def _mode(self) -> str:
        return "visual" if self._vis_on else ("vim" if self._vim_on else "insert")

    # ------------------------------------------------------------------
    # keyd listen subprocess
    # ------------------------------------------------------------------

    def _spawn_listener(self) -> bool:
        """Start keyd listen as a background subprocess."""
        if self._proc is not None:
            self._kill_listener()

        try:
            self._proc = subprocess.Popen(
                ["keyd", "listen"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            assert self._proc.stdout is not None
            os.set_blocking(self._proc.stdout.fileno(), False)
            if self._loop is not None:
                self._loop.add_reader(
                    self._proc.stdout.fileno(), self._on_stdout_data
                )
            return True
        except Exception as ex:
            print(f"[keyd] listen spawn failed: {ex}", file=sys.stderr)
            self._proc = None
            return False

    def _kill_listener(self) -> None:
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
        """Event-loop callback: keyd listen stdout has data."""
        if self._proc is None or self._proc.stdout is None:
            return
        try:
            raw = os.read(self._proc.stdout.fileno(), 65536)
            if not raw:
                self._on_listener_died()
                return
            self._buf += raw.decode("utf-8", errors="replace")
            while "\n" in self._buf:
                line, self._buf = self._buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                self._parse_line(line)
        except (BlockingIOError, OSError, ValueError):
            self._on_listener_died()

    def _on_listener_died(self) -> None:
        """Listener died — clean up and restart after a delay."""
        self._kill_listener()
        if self._loop is not None and not self._finalized:
            self._loop.call_later(2.0, self._spawn_listener)

    # ------------------------------------------------------------------
    # keyd listen line parser
    # ------------------------------------------------------------------

    def _parse_line(self, line: str) -> None:
        changed = False
        if line.startswith("/"):
            # Full state: /main or /main+vimmode or /main+vimmode+visual
            parts = line.split("/")[-1].split("+")
            layers = parts[1:] if len(parts) > 1 else []
            nv = "vimmode" in layers
            nvs = "visual" in layers
            changed = nv != self._vim_on or nvs != self._vis_on
            self._vim_on, self._vis_on = nv, nvs
        elif line == "+vimmode":
            changed = not self._vim_on
            self._vim_on = True
        elif line == "-vimmode":
            changed = self._vim_on
            self._vim_on = False
        elif line == "+visual":
            changed = not self._vis_on
            self._vis_on = True
        elif line == "-visual":
            changed = self._vis_on
            self._vis_on = False
        else:
            return  # unrecognised line

        if changed:
            self._update_display()

    # ------------------------------------------------------------------
    # Display update
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        in_vim_app = self._is_vim_app_focused()
        if in_vim_app:
            m = self._mode
            if m == "visual":
                self._external_text = ICON_VIS
                self.foreground = theme["red"]
            elif m == "vim":
                self._external_text = ICON_VIM
                self.foreground = theme["red"]
            else:
                self._external_text = ICON_INS
                self.foreground = theme["green"]
        else:
            self.foreground = theme["fg"]
        self.update(self._external_text if in_vim_app else "")

    # ------------------------------------------------------------------
    # Focus tracking
    # ------------------------------------------------------------------

    def _on_focus_change(self, client):
        if client is None:
            self._focused_app = None
        else:
            wm_class = client.get_wm_class()
            self._focused_app = wm_class[0] if wm_class else None
        self._update_display()

    # ------------------------------------------------------------------
    # Qtile lifecycle
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

        # Spawn keyd listen
        self._spawn_listener()

        # Track initial focus
        win = qtile.current_window
        if win is not None:
            wm_class = win.get_wm_class()
            if wm_class:
                self._focused_app = wm_class[0]
        self._update_display()

    def finalize(self):
        self._finalized = True
        self._kill_listener()
        hook.unsubscribe.client_focus(self._on_focus_change)
        base._TextBox.finalize(self)
