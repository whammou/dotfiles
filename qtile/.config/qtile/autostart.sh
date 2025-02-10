#!/usr/bin/bash

# Variables for current session
export QT_IM_MODULE=fcitx
export GTK_IM_MODULE=fcitx
export GLFW_IM_MODULE=ibus
export XMODIFIERS=@im=fcitx

# Pre-start tmux sessions
tmux-session

# Modify keyboard behaviours
xinput disable TPPS\/2\ IBM\ TrackPoint
setxkbmap -option caps:swapescape &
xinput disable "Synaptics TM3075-002" &
(
  sleep 2
  xmodmap $HOME/.Xmodmap 2>/tmp/xmodmap.errors
) &

# Window Composers
picom -b &>/dev/null &
unclutter a --start-hidden &

# Pre-start browsers
qutebrowser -R --nowindow &

# Pre-start input methods
fcitx5 -d &
