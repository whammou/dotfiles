if [ -n "$SSH_CONNECTION" ]; then
  export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/ssh_dbus.sock
fi
