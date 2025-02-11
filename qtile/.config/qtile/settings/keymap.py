from .keymaps.spawn import tmux_session_attach


keymap = [
    {
        "name": "qutebrowser",
        "prefix": "q",
        "cmd": [
            ["b", "qb"],
            ["p", "qb-url"],
            ["o", "qb_bookmark"],
        ],
    },
    {
        "name": "lobster",
        "prefix": "u",
        "cmd": [
            ["l", "kitty --hold -e 'lobsterfzf'"],
            ["S-l", "kitty --hold -e 'lobsterfzf_trending'"],
        ],
    },
    {
        "name": "orgmode",
        "prefix": "o",
        "cmd": [
            ["a", "kitty -e 'orgmode-agenda'"],
            ["t", "orgmode-todo"],
            ["c", "orgmode-capture"],
        ],
    },
    {
        "name": "yazi",
        "prefix": "f",
        "cmd": [
            ["h", "kitty --hold -e yazi $HOME"],
            ["s", "kitty --hold -e yazi /server/"],
        ],
    },
    {
        "name": "tmux",
        "prefix": "t",
        "cmd": tmux_session_attach(range(1, 10)),
    },
]
