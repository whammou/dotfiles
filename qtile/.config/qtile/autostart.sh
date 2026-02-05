#!/usr/bin/bash

qtile cmd-obj -o core -f hide_cursor &>/dev/null &
#unclutter a --start-hidden & # Hide cursor
#dunst &
fcitx5 -d &>/dev/null &    # Input method
tmux-session &>/dev/null & # Tmux sessions

#greenclip daemon & # Clipboard daemon
#xscreensaver --no-splash &
#daemon qutebrowser-daemon --name=qutebrowser-daemon -r & #Browser daemon
#xset s off && xset -dpms &
#daemon qutebrowser-daemon \
#  --name=qutebrowser-daemon \
#  --attempts=3 \
#  --delay=10 \
#  --limit=1 --safe \
#  --nocore \
#  --i -r &
#ntfyDesktop --desktopfile /home/whammou/ntfy &
#qutebrowser -R --nowindow &
