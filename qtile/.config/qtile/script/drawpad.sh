#!/bin/bash

# Get the current status of the touchpad
status=$(xinput list-props "VEIKK.INC VK430 Mouse" | grep "Device Enabled" | awk '{print $NF}')

# Toggle the touchpad based on its current status
if [ $status -eq 1 ]; then
    xinput disable "VEIKK.INC VK430 Mouse"
    echo "Touchpad disabled"
else
    xinput enable "VEIKK.INC VK430 Mouse"
    echo "Touchpad enabled"
fi
