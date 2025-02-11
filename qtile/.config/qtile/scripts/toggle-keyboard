#!/bin/bash

# Get the current state of the keyboard
state=$(xset -q | grep "Keyboard" | awk '{print $4}')

# Toggle the keyboard state
if [ "$state" == "on" ]; then
    xset -q | grep "Keyboard" | awk '{print $4="off"}'
else
    xset -q | grep "Keyboard" | awk '{print $4="on"}'
fi
