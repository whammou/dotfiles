#!/bin/bash

export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/ssh_dbus.sock
alacritty -e tmux-session

# WDM
picom --experimental-backends &>/dev/null &
nitrogen --restore &>/dev/null &

# Input
xinput --set-prop "SynPS/2 Synaptics TouchPad" "Device Accel Velocity Scaling" 1 &
xinput disable "SynPS/2 Synaptics TouchPad" &
setxkbmap -option caps:swapescape &
xbanish &
ibus &

# Sync
ngrok start --config ~/.config/ngrok/ngrok.yml --all &
mega-session &
syncthing --no-browser &


