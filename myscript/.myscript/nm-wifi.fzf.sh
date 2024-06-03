#!  /usr/bin/bash

  nmcli device wifi rescan > /dev/null
  ssid=$(nmcli device wifi list | tail -n +2 | grep -v '^  *\B--\B' | fzf -m | sed 's/^ *\*//' | awk '{print $1}')

  if [ "x$ssid" != "x" ]; then
    # check if the SSID has already a connection setup
    conn=$(nmcli con | grep "$ssid" | awk '{print $1}' | uniq)
    if [ "x$conn" = "x$ssid" ]; then
      echo "Please wait while switching to known network $ssid…"
      # if yes, bring up that connection
      nmcli con up id "$conn"
      name=$(iwgetid -r)
      notify-send -i " " "Network Manager" "Connected to $name"
    else
      echo "Please wait while connecting to new network $ssid…"
      # if not connect to it and ask for the password
      nmcli device wifi connect "$ssid"
      name=$(iwgetid -r)
      notify-send -i " " "Network Manager" "Connected to $name"
    fi
  fi

