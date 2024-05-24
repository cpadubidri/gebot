#!/bin/bash

# Command to open Google Earth Pro
google-earth-pro &

# Wait for the application to start
sleep 5

# Get the window ID of Google Earth Pro
window_id=$(wmctrl -lx | grep "google-earth" | awk '{print $1}')

# Check if the window ID was found
if [ -z "$window_id" ]; then
  echo "Google Earth Pro window not found!"
  exit 1
fi

# Move the window to the left half of the screen
wmctrl -ir $window_id -b remove,maximized_vert,maximized_horz
wmctrl -ir $window_id -e 0,0,0,960,1080

echo "Google Earth Pro is now minimized to the left half of the screen."
