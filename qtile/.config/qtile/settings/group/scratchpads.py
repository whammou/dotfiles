from libqtile.config import DropDown, KeyChord, EzKey
from libqtile.lazy import lazy


def scratchpad_layout(layout=[0.8, 0.8, 0.1, 0.1], preset="custom"):
    match preset:
        case "custom":
            return {
                "width": layout[0],
                "height": layout[1],
                "x": layout[2],
                "y": layout[3],
            }
        case "pad_extra_large":
            return {
                "width": 0.8,
                "height": 0.8,
                "x": 0.1,
                "y": 0.1,
            }
        case "pad_large":
            return {
                "width": 0.7,
                "height": 0.7,
                "x": 0.15,
                "y": 0.15,
            }
        case "pad_medium":
            return {
                "width": 0.6,
                "height": 0.6,
                "x": 0.2,
                "y": 0.2,
            }
        case "pad_small":
            return {
                "width": 0.45,
                "height": 0.8,
                "x": 0.275,
                "y": 0.1,
            }
        case "pad_prompt":
            return {
                "width": 0.45,
                "height": 0.04,
                "x": 0.275,
                "y": 0.48,
            }
        case "pad_list":
            return {
                "width": 0.45,
                "height": 0.2,
                "x": 0.275,
                "y": 0.4,
            }
        case "pad_typing":
            return {
                "width": 0.9985,
                "height": 0.25,
                "x": 0.00075,
                "y": 0,
            }
        case "power_menu":
            return {
                "width": 0.1,
                "height": 0.2,
                "x": 0.45,
                "y": 0.4,
            }


def dropdowns(keymap):
    dropdowns = []
    for package in keymap:
        for c in package["cmd"]:
            dropdowns.append(
                DropDown(
                    c[1],
                    c[1],
                    opacity=1.0,
                    on_focus_lost_hide=False,
                    **scratchpad_layout(preset=c[2]),
                )
            )
    return dropdowns


def scratchpad_keys(mod, trigger, keymap):
    prefix_bind = []
    for package in keymap:
        cmd_bind = []
        for p in package["prefix"]:
            key_bind = []
            for c in package["cmd"]:
                key_bind.append(
                    EzKey(
                        c[0],
                        lazy.group["scratchpad"].dropdown_toggle(c[1]),
                        lazy.window.set_opacity(1),
                    )
                )
            cmd_bind.append(KeyChord([], p, key_bind))
        prefix_bind.extend(cmd_bind)
    position_bind = KeyChord(mod, trigger, prefix_bind)
    return [position_bind]
