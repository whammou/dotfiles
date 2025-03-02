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
        on_focus_lost_hide=False,
    ),
    DropDown(
        "adapter",
        "kitty --class=pwd_prompt -o font.size=10 -e adapter-switch",
        width=0.45,
        height=0.04,
        x=0.275,
        y=0.48,
    ),
]
dropdown.extend(dropdowns(keymap))

groups.append(ScratchPad("scratchpad", dropdown))
