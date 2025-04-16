from libqtile.config import EzKey, KeyChord
from libqtile.lazy import lazy


def tmux_session_attach(session_range):
    session_bind = []
    for i in session_range:
        session_bind.append(
            [str(i), " ".join(["kitty -e tmux-session-attach", str(i)]), "pad_large"]
        )
    return session_bind


def spawn_position(mod, trigger, keymap, orientation, **spawn):
    prefix_bind = []
    for package in keymap:
        cmd_bind = []
        for p in package["prefix"]:
            key_bind = []
            for c in package["cmd"]:
                # print(c[0], c[1], spawn)
                key_bind.append(
                    EzKey(c[0], lazy.layout.spawn_split(c[1], orientation, **spawn))
                )
            # print(p, key_bind)
            cmd_bind.append(KeyChord([], p, key_bind))
        # print(cmd_bind)
        prefix_bind.extend(cmd_bind)
    position_bind = KeyChord(mod, trigger, prefix_bind)
    # print(position_bind)
    return [position_bind]


def spawn_tab(mod, trigger, keymap, **spawn):
    prefix_bind = []
    for package in keymap:
        cmd_bind = []
        for p in package["prefix"]:
            key_bind = []
            for c in package["cmd"]:
                # print(c[0], c[1])
                key_bind.append(EzKey(c[0], lazy.layout.spawn_tab(c[1], **spawn)))
            # print(p, key_bind)
            cmd_bind.append(KeyChord([], p, key_bind))
        # print(cmd_bind)
        prefix_bind.extend(cmd_bind)
    position_bind = KeyChord(mod, trigger, prefix_bind)
    # print(position_bind)
    return [position_bind]
