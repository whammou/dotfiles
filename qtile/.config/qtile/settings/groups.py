from libqtile.config import Group
from libqtile.lazy import lazy

from .keys import mod, keys
from .group.scratchpads import scratchpads


groups = [Group(i) for i in "1"]
groups.append(scratchpads)


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
