#!/bin/bash

# Get the current state of the monitor
state=$(xrandr --query | grep " connected" | awk '{print $2}')

# Check if the monitor is currently on or off
if [ "$state" == "connected" ]; then
    # If the monitor is on, turn it off
    xrandr --output $(xrandr --query | grep " connected" | awk '{print $1}') --off
    echo "Monitor turned off"
else
    # If the monitor is off, turn it on
    xrandr --output $(xrandr --query | grep " connected" | awk '{print $1}') --auto
    echo "Monitor turned on"
fi
