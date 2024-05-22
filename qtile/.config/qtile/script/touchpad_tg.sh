#!/bin/bash

# Get the current status of the touchpad
status=$(xinput list-props 9 | grep "Device Enabled" | awk '{print $NF}')

# Toggle the touchpad based on its current status
if [ $status -eq 1 ]; then
    xinput disable 9
    echo "Touchpad disabled"
else
    xinput enable 9
    echo "Touchpad enabled"
fi
