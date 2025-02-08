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
    position_bind = KeyChord([mod], orientation, prefix_bind)
    #print(position_bind)
    return [position_bind]
