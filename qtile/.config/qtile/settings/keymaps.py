from .key.spawn import tmux_session_attach
from .path import in_terminal


keymap = [
    {
        "name": "qutebrowser",
        "prefix": "q",
        "cmd": [
            ["t", "qutebrowser_tabbed", "pad_large"],
            [
                "i",
                "qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py",
                "pad_large",
            ],
            ["p", "qb-url", "pad_large"],
            ["b", "qb chat.beeper.com", "pad_large"],
        ],
    },
    {
        "name": "orgmode",
        "prefix": "o",
        "cmd": [
            ["a", in_terminal("orgmode-agenda"), "pad_large"],
            ["n", in_terminal("orgmode-notes"), "pad_large"],
            ["c", in_terminal("orgmode-capture"), "pad_large"],
            ["t", in_terminal("orgmode-todo"), "pad_large"],
        ],
    },
    {
        "name": "yazi",
        "prefix": "f",
        "cmd": [
            ["h", in_terminal("yazi $HOME"), "pad_medium"],
            ["s", in_terminal("yazi /server/"), "pad_medium"],
        ],
    },
    {
        "name": "tmux",
        "prefix": "t",
        "cmd": tmux_session_attach(range(0, 10)),
    },
    {
        "name": "monitor",
        "prefix": "m",
        "cmd": [
            ["p", in_terminal("btm"), "pad_large"],
            ["b", in_terminal("monitor-battery"), "pad_list"],
            [
                "S-b",
                in_terminal("sudo tlp recalibrate", parameters="--hold"),
                "pad_list",
            ],
            ["v", in_terminal("monitor-voltage"), "pad_list"],
            ["c", in_terminal("watch-cpu"), "pad_list"],
            ["g", in_terminal("sudo intel_gpu_top"), "pad_small"],
        ],
    },
    {
        "name": "utility",
        "prefix": "u",
        "cmd": [
            ["a", in_terminal("anifzf"), "pad_small"],
            ["d", "discord", "pad_large"],
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
            [
                "y",
                in_terminal("magic-tape.sh", parameters="--hold"),
                "pad_large",
            ],
            [
                "m",
                in_terminal("sh magic-tape.sh", parameters="--hold"),
                "pad_large",
            ],
            [
                "S-y",
                "firefox 'https://youtube.com/account'",
                "pad_small",
            ],
        ],
    },
]
