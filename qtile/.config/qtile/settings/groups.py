from libqtile.config import Group, ScratchPad
from libqtile.lazy import lazy

from .keys import mod, keys
from .group.scratchpads import dropdowns, scratchpad_keys
from .keymaps import keymap


groups = [Group(i) for i in "1"]
groups.append(ScratchPad("scratchpad", dropdowns(keymap)))


# for i in groups:
#     keys.extend(
#         [
#             Key(
#                 [mod],
#                 i.name,
#                 lazy.group[i.name].toscreen(),
#                 desc=f"Switch to group {i.name}",
#             ),
#             Key(
#                 [mod, "shift"],
#                 i.name,
#                 lazy.window.togroup(i.name, switch_group=True),
#                 desc=f"Switch to & move focused window to group {i.name}",
#             ),
#         ]
#     )
