from .key.spawn import tmux_session, ssh_session
from .path import in_terminal


keymap = [
    {
        "name": "qutebrowser",
        "prefix": "b",
        "cmd": [
            ["s", "qutebrowser_search", "pad_large"],
            ["t", "qutebrowser_tabbed", "pad_large"],
            [
                "i",
                "qutebrowser -T -C /home/whammou/.config/qutebrowser/config.py --set tabs.tabs_are_windows false",
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
                "o",
                in_terminal(
                    "opencode attach -p Unlimitednova199- https://opencode.whammou.dedyn.io --dir /home/whammou --continue",
                    parameters="--hold",
                    app_id="opencode-attach",
                ),
                "pad_small",
            ],
            [
                "S-o",
                in_terminal(
                    "opencode",
                    parameters="--hold",
                    app_id="opencode",
                ),
                "pad_small",
            ],
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
            ["a", in_terminal("orgmode-agenda", app_id="org-agenda"), "pad_large"],
            [
                "S-n",
                "kitty --session /home/whammou/Workspace/kitty-session/test.session",
                "pad_extra_large",
            ],
            ["l", in_terminal("orgmode-backlog", app_id="org-backlog"), "pad_large"],
            ["z", in_terminal("orgmode-browse", app_id="org-browse"), "pad_large"],
            ["o", in_terminal("orgmode-super-agenda", app_id="org-super-agenda"), "pad_large"],
            ["g", in_terminal("lazygit -p /home/whammou/Journal", app_id="lazygit-journal"), "pad_large"],
            ["c", in_terminal("orgmode-capture", app_id="org-capture"), "pad_small"],
            ["d", in_terminal("orgroam-capture", app_id="org-roam-capture"), "pad_small"],
            ["m", in_terminal("orgmode-search", app_id="org-search"), "pad_large"],
        ],
    },
    {
        "name": "yazi",
        "prefix": "e",
        "cmd": [
            ["h", in_terminal("yazi $HOME", app_id="yazi"), "pad_medium"],
            ["s", in_terminal("yazi sftp://homelab", app_id="yazi-sftp"), "pad_medium"],
            ["n", in_terminal("yazi /home/whammou/Journal", app_id="yazi-journal"), "pad_large"],
        ],
    },
    {
        "name": "tmux",
        "prefix": "t",
        "cmd": tmux_session(range(0, 10), "kitty -e tmux-session-attach"),
    },
    {
        "name": "ssh",
        "prefix": "s",
        "cmd": ssh_session(range(0, 10)),
    },
    {
        "name": "monitor",
        "prefix": "m",
        "cmd": [
            ["p", in_terminal("btm", app_id="btm"), "pad_large"],
            ["b", in_terminal("monitor-battery", app_id="mon-battery"), "pad_list"],
            [
                "S-b",
                in_terminal("sudo tlp recalibrate", parameters="--hold", app_id="tlp-recalibrate"),
                "pad_list",
            ],
            ["v", in_terminal("monitor-voltage", app_id="mon-voltage"), "pad_list"],
            ["c", in_terminal("watch-cpu", app_id="watch-cpu"), "pad_list"],
            ["g", in_terminal("nvtop", app_id="nvtop"), "pad_small"],
            ["d", in_terminal("ncdu --color dark /", app_id="ncdu"), "pad_small"],
            ["m", in_terminal("watch -n 1 xset q", app_id="xset"), "pad_small"],
            ["s", in_terminal("sysz --user", parameters="--hold", app_id="sysz-user"), "pad_medium"],
            ["e", in_terminal("fzf-emoji", app_id="fzf-emoji"), "pad_medium"],
            ["S-s", in_terminal("sysz --system", parameters="--hold", app_id="sysz-system"), "pad_medium"],
        ],
    },
    {
        "name": "utility",
        "prefix": "u",
        "cmd": [
            # ["s", in_terminal("chess-tui --engine-path /sbin/stockfish"), "pad_small"],
            ["b", in_terminal("bluetuith", app_id="bluetuith"), "pad_small"],
            [
                "y",
                in_terminal("yt-x", parameters="--title='YTX | Youtube'", app_id="yt-x"),
                "pad_small",
            ],
            ["g", in_terminal("lazygit -p /home/whammou/dotfiles/", app_id="lazygit-dotfiles"), "pad_large"],
            ["e", in_terminal("nvim", app_id="nvim"), "pad_large"],
            [
                "u",
                in_terminal("sh 'paru -Syy && paru -Syu' ; alert", parameters="--hold", app_id="sys-upgrade"),
                "pad_large",
            ],
            [
                "S-s",
                in_terminal("chessterm --black_engine=/sbin/stockfish", app_id="chessterm"),
                "pad_small",
            ],
            ["n", "rnote", "pad_extra_large"],
            ["s", "wlr-which-key", "pad_extra_large"],
            ["r", in_terminal("newsboat", app_id="newsboat"), "pad_large"],
            ["S-n", in_terminal("notification_history", app_id="notif-history"), "pad_small"],
            ["m", in_terminal("neomutt", app_id="neomutt"), "pad_large"],
            ["S-m", in_terminal("mangal", app_id="mangal"), "pad_small"],
            ["d", in_terminal("dict", app_id="dict"), "pad_small"],
            ["a", in_terminal("anifzf", app_id="anifzf"), "pad_small"],
            ["S-a", in_terminal("ani-cli -c", app_id="ani-cli"), "pad_small"],
            [
                "t",
                in_terminal(
                    "tt --theme=mine --multi --nohighlight",
                    parameters="--title='TT | Typing' -o font_size=20",
                    app_id="typing-test",
                ),
                "pad_typing",
            ],
            # ["l", in_terminal("lobster"), "pad_small"],
            # ["S-l", in_terminal("lobster -c"), "pad_small"],
            ["l", in_terminal("kari", app_id="kari"), "pad_small"],
            [
                "c",
                in_terminal(
                    ".venv/calculator/bin/python -i .local/bin/calc",
                    parameters="--title='CAL | Calculator'",
                    app_id="calculator",
                ),
                "pad_small",
            ],
            [
                "S-y",
                "firefox 'https://youtube.com/account'",
                "pad_small",
            ],
        ],
    },
]
