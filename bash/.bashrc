# Source session environment (single source of truth in ~/.profile)
# Guard: only run in interactive shells (avoids breaking Wayland compositor startup)
[[ $- != *i* ]] && return

[ -f "$HOME/.profile" ] && . "$HOME/.profile"

PS1='[\u@\h \W]\$ '
[ -f "$HOME/.config/fzf/fzf-lua-mimic.sh" ] && source "$HOME/.config/fzf/fzf-lua-mimic.sh"
eval "$(starship init bash)"

# Machine-local overrides (create ~/.env per-machine for secrets/addresses)
[ -f "$HOME/.env" ] && source "$HOME/.env"

if [ -n "$SSH_CONNECTION" ]; then
  curl \
    -H "t:Remote Warning" \
    -d "$(cat /proc/sys/kernel/hostname): SSH Login Warning
Date: $(date -d '+7 hours' '+%FT%H:%M:%S')
User: $USER
IP Address: ${SSH_CLIENT%% *}
" \
    https://ntfy.sh/whammou-alert
fi
