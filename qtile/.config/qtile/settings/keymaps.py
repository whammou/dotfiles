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
        ],
    },
    {
        "name": "chat",
        "prefix": "c",
        "cmd": [
            [
                "b",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/chat.beeper.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                chat.beeper.com",
                "pad_large",
            ],
            [
                "d",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/discord.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                discord.com/app",
                "pad_large",
            ],
            ["S-d", "discord", "pad_large"],
            [
                "z",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/chat.zalo.me \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                chat.zalo.me/",
                "pad_large",
            ],
        ],
    },
    {
        "name": "ai",
        "prefix": "a",
        "cmd": [
            [
                "g",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/chatgpt.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                chatgpt.com",
                "pad_large",
            ],
            [
                "e",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/gemini.google.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                gemini.google.com",
                "pad_large",
            ],
        ],
    },
    {
        "name": "google-suit",
        "prefix": "g",
        "cmd": [
            [
                "d",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/docs.google.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                docs.google.com",
                "pad_large",
            ],
            [
                "p",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/presentation.google.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                docs.google.com/presentation",
                "pad_large",
            ],
            [
                "s",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/spreadsheets.google.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                docs.google.com/spreadsheets",
                "pad_large",
            ],
            [
                "m",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/meet.google.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                meet.google.com",
                "pad_large",
            ],
            [
                "f",
                "qutebrowser --basedir=/home/whammou/.cache/qutebrowser/simplepdf.com \
                --config-py=/home/whammou/.config/qutebrowser/config.py \
                simplepdf.com/editor",
                "pad_large",
            ],
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
            ["d", in_terminal("ncdu --color dark"), "pad_small"],
        ],
    },
    {
        "name": "utility",
        "prefix": "u",
        "cmd": [
            ["d", "rnote", "pad_extra_large"],
            ["a", in_terminal("anifzf"), "pad_small"],
            [
                "t",
                in_terminal(
                    "tt --theme=mine --multi --nohighlight",
                    parameters="--title='Typing - tt' -o font_size=20",
                ),
                "pad_typing",
            ],
            ["l", in_terminal("lobster"), "pad_small"],
            ["S-l", in_terminal("lobster -c"), "pad_small"],
            [
                "c",
                in_terminal(".venv/calculator/bin/python -i /usr/local/bin/calc"),
                "pad_small",
            ],
            [
                "y",
                in_terminal(
                    "magic-tape.sh", parameters="--title='Youtube - magic-tape'"
                ),
                "pad_large",
            ],
            [
                "m",
                in_terminal(
                    "sh magic-tape.sh", parameters="--title='Youtube-Music magic-tape'"
                ),
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
