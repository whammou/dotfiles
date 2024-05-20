#!/bin/bash

# Get the current status of the touchpad
status=$(xinput list-props "SynPS/2 Synaptics TouchPad" | grep "Device Enabled" | awk '{print $NF}')

# Toggle the touchpad based on its current status
if [ $status -eq 1 ]; then
    xinput disable "SynPS/2 Synaptics TouchPad"
    echo "Touchpad disabled"
else
    xinput enable "SynPS/2 Synaptics TouchPad"
    echo "Touchpad enabled"
fi
