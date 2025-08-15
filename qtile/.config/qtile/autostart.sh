#!/usr/bin/bash

# Disable mouse and rebind keys
xinput disable TPPS\/2\ IBM\ TrackPoint
setxkbmap -option caps:swapescape
xinput disable "Synaptics TM3075-002" &
xmodmap $HOME/.Xmodmap 2>/tmp/xmodmap.errors

picom -b &>/dev/null &       # Window compositor
unclutter a --start-hidden & # Hide cursor
fcitx5 -d &                  # Input method
tmux-session                 # Tmux sessions
greenclip daemon &           # Clipboard daemon
#daemon qutebrowser-daemon --name=qutebrowser-daemon -r & #Browser daemon
daemon qutebrowser-daemon --name=qutebrowser-daemon --attempts=3 --delay=10 --safe -r &
#qutebrowser -R --nowindow &
