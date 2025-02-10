from libqtile.config import EzKey, KeyChord
from libqtile.lazy import lazy


mod = "mod4"

def spawn_position(keymap, orientation, position):
    prefix_bind = []
    for package in keymap:
        cmd_bind = []
        for p in package["prefix"]:
            key_bind =[]
            for c in package["cmd"]:
                #print(c[0], c[1])
                key_bind.append(EzKey(c[0], lazy.layout.spawn_split(c[1], orientation, position=position)))
            #print(p, key_bind)
            cmd_bind.append(KeyChord([], p, key_bind))
        #print(cmd_bind)
        prefix_bind.extend(cmd_bind)
    match position:
        case "next":
            position_bind = KeyChord([mod], orientation, prefix_bind)
        case "previous":
            position_bind = KeyChord([mod, "Shift"], orientation, prefix_bind)
    #print(position_bind)
    return [position_bind]


def spawn_tab(keymap, newlevel=False):
    prefix_bind = []
    for package in keymap:
        cmd_bind = []
        for p in package["prefix"]:
            key_bind =[]
            for c in package["cmd"]:
                #print(c[0], c[1])
                key_bind.append(EzKey(c[0], lazy.layout.spawn_tab(c[1], new_level=newlevel)))
            #print(p, key_bind)
            cmd_bind.append(KeyChord([], p, key_bind))
        #print(cmd_bind)
        prefix_bind.extend(cmd_bind)
    match newlevel:
        case False:
            position_bind = KeyChord([mod], "t", prefix_bind)
        case True:
            position_bind = KeyChord([mod, "Shift"], "t", prefix_bind)
    #print(position_bind)
    return [position_bind]
