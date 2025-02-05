from libqtile.config import Key, Group
from libqtile.lazy import lazy
from .keys import mod, keys


groups = [Group(i) for i in "123456789"]

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
