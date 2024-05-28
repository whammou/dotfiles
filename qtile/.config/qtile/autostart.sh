#!/bin/bash

# WDM
picom --experimental-backends &
nitrogen --restore &

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


