if [ -n "$SSH_CONNECTION" ]; then
  export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/ssh_dbus.sock
  curl \
    -H "t:Terminal" \
    -d " $(cat /proc/sys/kernel/hostname) :: SSH Login Attempt
  Date: $(date -d '+7 hours' '+%FT%H:%M:%S')
  User: $USER
  Host: $(cat /proc/sys/kernel/hostname)
  IP Address: ${SSH_CLIENT%% *}
  " \
    https://ntfy.sh/whammou_alert
fi
