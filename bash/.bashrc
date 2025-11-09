if [ -n "$SSH_CONNECTION" ]; then
  #export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/ssh_dbus.sock
  curl \
    -H "t:Remote Warning" \
    -d "<b>$(cat /proc/sys/kernel/hostname)</b>: SSH Login Warning
Date: $(date -d '+7 hours' '+%FT%H:%M:%S')
User: $USER
IP Address: ${SSH_CLIENT%% *}
" \
    https://ntfy.sh/whammou-alert
fi
