from libqtile.config import Key, Group, ScratchPad
from libqtile.lazy import lazy
from .keys import mod, keys


def base(wd=0.45, he=0.8):
    return {
        "width": wd,
        "height": he,
        "x": 0.275,
        "y": 0.4,
    }

groups = [Group(i) for i in "1"]

#scratchpad = ScratchPad("scratchpad", [DropDown()])

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
