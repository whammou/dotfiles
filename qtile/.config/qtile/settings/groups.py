from libqtile.config import Group, ScratchPad, DropDown

from .group.scratchpads import dropdowns
from .keymaps import keymap


groups = [Group(i) for i in "1"]

dropdown = [
    DropDown(
        "nmfzf",
        "kitty --class=nmcli-fzf -e bash /usr/local/bin/nmwifi-fzf",
        width=0.6,
        height=0.8,
        x=0.2,
        y=0.1,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
    DropDown(
        "a2ln",
        "kitty -e a2ln pair",
        width=0.6,
        height=0.8,
        x=0.2,
        y=0.1,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
    DropDown(
        "adapter",
        "kitty --class=pwd_prompt -o font.size=10 -e adapter-switch",
        width=0.45,
        height=0.04,
        x=0.275,
        y=0.48,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
    DropDown(
        "powermenu",
        "kitty --title=Power -o font_size=17 -e power-menu",
        width=0.2,
        height=0.4,
        x=0.4,
        y=0.2,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
    DropDown(
        "calendar",
        "kitty --hold --title=calendar -e 'khal calendar | less'",
        width=0.3,
        height=0.4,
        x=0.7,
        y=0,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
    DropDown(
        "samba",
        "kitty --title='Toggle samba-drive' -e smb-toggle",
        width=0.45,
        height=0.04,
        x=0.275,
        y=0.48,
        opacity=1.0,
        on_focus_lost_hide=False,
    ),
]
dropdown.extend(dropdowns(keymap))

groups.append(ScratchPad("scratchpad", dropdown))
