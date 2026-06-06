"""
nvim-whichkeys style keybinding popup for Qtile.

Shows a themed cheat-sheet overlay with all available keybindings
organized by functional group. Triggered via `mod+/`.

The spawn-apps section is built dynamically from `keymaps.py` — adding
a new entry there automatically appears in the popup.  Other sections
(key definitions spread across `key/*.py` as `Key` / `EzKey` / `KeyChord`
objects) are kept as static summaries.
"""

from qtile_extras.popup import PopupRelativeLayout, PopupText

from .theme import colors


# ── Theme helpers ──────────────────────────────────────────────────────────


def _hex(name):
    return colors[name][0]


# ── Popup singleton (toggle on mod+/) ──────────────────────────────────────

_POPUP = None


def _close_popup():
    global _POPUP
    if _POPUP is not None:
        try:
            _POPUP.kill()
        except Exception:
            pass
        _POPUP = None


# ── Static group definitions (non-spawn sections) ──────────────────────────

STATIC_GROUPS = [
    # Column 1
    {
        "title": "  CORE WM",
        "color": "blue",
        "items": [
            ("C-r", "Reload config"),
            ("q", "Kill focused window"),
            ("S-q", "Kill process (rofi)"),
            ("r", "Spawn command prompt"),
            ("n", "Normalize layout"),
            ("S-n", "Normalize all columns"),
        ],
    },
    {
        "title": "  WINDOW OPS",
        "color": "green",
        "items": [
            ("C-h", "Resize left"),
            ("C-l", "Resize right"),
            ("C-k", "Resize up"),
            ("C-j", "Resize down"),
            ("S-h", "Swap window left"),
            ("S-l", "Swap window right"),
            ("S-k", "Swap window up"),
            ("S-j", "Swap window down"),
            ("o", "Select outer container"),
            ("i", "Select inner container"),
            ("Tab", "Focus previous window"),
            ("S-Esc", "Toggle tiling/floating"),
            ("z", "Toggle fullscreen"),
            ("S-z", "Toggle floating"),
        ],
    },
    {
        "title": "  FLOATING WINDOWS",
        "color": "yellow",
        "items": [
            (".", "Next floating"),
            (",", "Prev floating"),
            ("h/j/k/l", "Move floating"),
            ("m", "Keep below"),
            ("A-S-0", "All floats front"),
            ("C-Esc", "Hide scratchpads"),
            ("S-C-Esc", "Hide all + floats"),
        ],
    },
    {
        "title": "  TABS / LAYERS",
        "color": "cyan",
        "items": [
            ("1-9", "Focus tab at level N"),
            ("A-1-9", "Focus visible window N"),
            ("0", "Focus floating window N"),
            ("S-t/S-n/S-p", "Spawn tab"),
        ],
    },
    # Column 2
    {
        "title": "  CONTAINER SELECT  (mod + w)",
        "color": "orange",
        "items": [
            ("v", "Split vertical"),
            ("x", "Split horizontal"),
            ("t", "Tab"),
            ("S-t", "Tab (new level)"),
            ("w", "Toggle select mode"),
            ("h/j/k/l", "Focus direction"),
            ("o", "Pull out"),
            ("m", "Merge -> hjkl"),
            ("i", "Push in -> hjkl"),
        ],
    },
    {
        "title": "  SPAWN POSITIONS",
        "color": "orange",
        "items": [
            ("mod+v", "Split right"),
            ("mod+x", "Split below"),
            ("S-v", "Split left"),
            ("S-x", "Split above"),
        ],
    },
    {
        "title": "  FUNCTIONAL KEYS",
        "color": "red",
        "items": [
            ("Vol keys", "Volume 5% (S=1%)"),
            ("Bright keys", "Brightness 5%"),
            ("Media keys", "Play/Pause/Next/Prev"),
            ("Print", "Screenshot (S=gui)"),
            ("Delete", "Power menu (rofi)"),
            ("Space", "Toggle trackpoint"),
            ("Home/End", "Notifications control"),
            ("A-C-v", "Clipboard history"),
        ],
    },
]


# ── Dynamic spawn section (from keymaps.py) ────────────────────────────────


def _build_spawn_groups():
    """Build app-spawn groups from the live `keymap` list.

    Adding/removing entries in ``keymaps.py`` is reflected here
    automatically — no need to touch this file.
    """
    from .keymaps import keymap

    items = []
    for pkg in keymap:
        sub_keys = ", ".join(c[0] for c in pkg["cmd"])
        desc = pkg["name"]
        # attach sub-key list when it's short enough to fit
        if len(sub_keys) < 24:
            desc += f"  [{sub_keys}]"
        items.append((pkg["prefix"], desc))

    return [
        {
            "title": "  SPAWN APPS  (mod + s / f / v / x / t)",
            "color": "purple",
            "items": items,
        },
    ]


# ── Compose final groups ───────────────────────────────────────────────────


def _get_groups():
    """Return the full groups list, mixing static + dynamic sections.

    Column 1: Core WM, Window Ops, Floating, Tabs/Layers
    Column 2: Spawn (dynamic), Container, Positions, Functional
    """
    spawn = _build_spawn_groups()
    # Insert spawn right after the Column-1 groups (index 4 in the
    # combined list where column boundary lies).
    groups = list(STATIC_GROUPS)
    groups.insert(4, spawn[0])
    return groups


# ── Layout constants ───────────────────────────────────────────────────────

TOP_MARGIN = 0.015
GROUP_GAP = 0.005
HEADER_H = 0.026
ROW_H = 0.022
COL1_X = 0.015
COL2_X = 0.50
COL_W = 0.475
FONT = "HasklugNerdFont"
FONT_BOLD = "HasklugNerdFont Bold"
FONT_SIZE = 18
HEADER_FONT_SIZE = 20


def _build_controls():
    """Build PopupText controls arranged in two columns."""
    controls = []
    groups = _get_groups()
    mid = (len(groups) + 1) // 2
    col1 = groups[:mid]
    col2 = groups[mid:]

    for col_idx, column in enumerate([col1, col2]):
        x = COL1_X if col_idx == 0 else COL2_X
        y = TOP_MARGIN

        for group in column:
            controls.append(
                PopupText(
                    text=group["title"],
                    pos_x=x,
                    pos_y=y,
                    width=COL_W,
                    height=HEADER_H,
                    font=FONT_BOLD,
                    fontsize=HEADER_FONT_SIZE,
                    foreground=_hex(group["color"]),
                )
            )
            y += HEADER_H

            for key_label, desc in group["items"]:
                controls.append(
                    PopupText(
                        text=f"{key_label:<8}{desc}",
                        pos_x=x,
                        pos_y=y,
                        width=COL_W,
                        height=ROW_H,
                        font=FONT,
                        fontsize=FONT_SIZE,
                        foreground=_hex("fg"),
                    )
                )
                y += ROW_H

            y += GROUP_GAP

    return controls


def show_which_key(qtile):
    """Toggle the which-key overlay.

    First press shows the popup.  Second press (or Escape / click) hides it.
    Escape works because we insert a focusable background control which
    enables keyboard event capture on the popup window.
    """
    global _POPUP

    if _POPUP is not None:
        _close_popup()
        return

    controls = _build_controls()

    controls.insert(
        0,
        PopupText(
            text="",
            pos_x=0,
            pos_y=0,
            width=1,
            height=1,
            can_focus=True,
        ),
    )

    layout = PopupRelativeLayout(
        qtile,
        width=1200,
        height=700,
        controls=controls,
        background=_hex("bg0") + "DD",
        initial_focus=None,
        close_on_click=True,
    )
    layout.show(centered=True)

    _POPUP = layout
