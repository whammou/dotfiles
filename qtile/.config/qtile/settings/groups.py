from libqtile.config import Group, ScratchPad, DropDown

from .group.scratchpads import dropdowns
from .keymaps import keymap


groups = [Group(i) for i in "1"]

dropdown = [
    DropDown(
        "nmfzf",
        "kitty --class=nmcli-fzf -e bash /usr/local/bin/nmwifi-fzf",
        width=0.45,
        height=0.8,
        x=0.275,
        y=0.1,
    ),
    DropDown(
        "adapter",
        "kitty --class=pwd_prompt -o font.size=10 -e adapter-switch",
        width=0.45,
        height=0.04,
        x=0.275,
        y=0.48,
    ),
    DropDown(
        "powermenu",
        "kitty --class=powermenu -e power-menu",
        width=0.1,
        height=0.2,
        x=0.45,
        y=0.4,
    ),
    DropDown(
        "terminal-tmux",
        "kitty --title='Session 0 - tmux' -e tmux new -A -s 0",
        width=0.8,
        height=0.8,
        x=0.1,
        y=0.1,
    ),
]
dropdown.extend(dropdowns(keymap))

groups.append(ScratchPad("scratchpad", dropdown))
