from .key.spawn import tmux_session_attach
from .path import in_terminal


keymap = [
    {
        "name": "qutebrowser",
        "prefix": "q",
        "cmd": [
            ["b", "qb", "pad_large"],
            ["p", "qb-url", "pad_large"],
            [
                "i",
                "qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py",
                "pad_large",
            ],
            [
                "d",
                "qutebrowser --target=window -B /home/whammou/.config/qutebrowser/app/ https://discord.com/app",
                "pad_large",
            ],
        ],
    },
    {
        "name": "orgmode",
        "prefix": "o",
        "cmd": [
            ["a", in_terminal("orgmode-agenda"), "pad_large"],
            ["t", in_terminal("orgmode-todo"), "pad_large"],
            ["c", in_terminal("orgmode-capture"), "pad_large"],
        ],
    },
    {
        "name": "yazi",
        "prefix": "f",
        "cmd": [
            ["h", in_terminal("yazi $HOME"), "pad_medium"],
            ["s", in_terminal("yazi /server/"), "pad_medium"],
            ["S-s", in_terminal("smb-mount"), "pad_prompt"],
            ["S-h", in_terminal("smb-umount"), "pad_prompt"],
        ],
    },
    {
        "name": "tmux",
        "prefix": "t",
        "cmd": tmux_session_attach(range(1, 10)),
    },
    {
        "name": "monitor",
        "prefix": "m",
        "cmd": [
            ["p", in_terminal("btm"), "pad_large"],
            ["b", in_terminal("monitor-battery"), "pad_list"],
            ["v", in_terminal("monitor-voltage"), "pad_list"],
            ["c", in_terminal("watch-cpu"), "pad_list"],
        ],
    },
    {
        "name": "utility",
        "prefix": "u",
        "cmd": [
            ["a", in_terminal("anifzf"), "pad_small"],
            [
                "t",
                in_terminal(
                    "tt --theme=mine --multi --nohighlight",
                    parameters="-o font_size=20",
                ),
                "pad_typing",
            ],
            ["l", in_terminal("lobsterfzf"), "pad_small"],
            ["S-l", in_terminal("lobsterfzf_trending"), "pad_small"],
            [
                "c",
                in_terminal(".venv/calculator/bin/python -i /usr/local/bin/calc"),
                "pad_small",
            ],
            # ["m", in_terminal("ytfzf-music"), "pad_small"],
            # ["y", in_terminal("ytfzf-video"), "pad_large"],
            # ["S-y", in_terminal("ytfzf-thumbnail"), "pad_large"],
            [
                "y",
                in_terminal(
                    "tmux -c 'yt-x --preview'",
                    parameters="--hold --title='yt-x (Thumbnail)'",
                ),
                "pad_large",
            ],
            [
                "S-y",
                in_terminal("tmux -c yt-x", parameters="--title='yt-x'"),
                "pad_large",
            ],
            [
                "S-s",
                in_terminal("sh smb-mount", parameters="-o font.size=10"),
                "pad_prompt",
            ],
            [
                "S-h",
                in_terminal("sh smb-umount", parameters="-o font.size=10"),
                "pad_prompt",
            ],
        ],
    },
]
