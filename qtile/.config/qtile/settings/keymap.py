from .keymaps.spawn import tmux_session_attach
from .path import script_path, run_script, in_terminal


keymap = [
    {
        "name": "qutebrowser",
        "prefix": "q",
        "cmd": [
            ["b",   "qb"],
            ["p",   "qb-url"],
            ["S-p", "qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py"]
        ],
    },
    {
        "name": "orgmode",
        "prefix": "o",
        "cmd": [
            ["a", in_terminal("orgmode-agenda")],
            ["t", in_terminal("orgmode-todo")],
            ["c", in_terminal("orgmode-capture")],
        ],
    },
    {
        "name": "yazi",
        "prefix": "f",
        "cmd": [
            ["h", in_terminal("yazi $HOME")],
            ["s", in_terminal("yazi /server/")],
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
            ["p", in_terminal("btm")],
            ["b", in_terminal("monitor-battery")],
            ["v", in_terminal("monitor-voltage")],
            ["c", in_terminal("watch-cpu")],
        ],
    },
    {
        "name": "utility",
        "prefix": "u",
        "cmd": [
            ["a",   in_terminal("anifzf")],
            ["t",   in_terminal("tt --theme=mine --multi --nohighlight", parameters="-o font_size=20")],
            ["l",   in_terminal("lobsterfzf")],
            ["S-l", in_terminal("lobsterfzf")],
            ["c",   in_terminal(".venv/calculator/bin/python -i /usr/local/bin/calc")],
            ["m",   in_terminal("ytfzf-music")],
            ["y",   in_terminal("ytfzf-video")],
            ["S-y", in_terminal("ytfzf-thumbnail")],
        ],
    },
]
