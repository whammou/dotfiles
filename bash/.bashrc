# Source session environment (single source of truth in ~/.profile)
# Guard: only run in interactive shells (avoids breaking Wayland compositor startup)
[[ $- != *i* ]] && return

[ -f "$HOME/.profile" ] && . "$HOME/.profile"

PS1='[\u@\h \W]\$ '
[ -f "$HOME/.config/fzf/fzf-lua-mimic.sh" ] && source "$HOME/.config/fzf/fzf-lua-mimic.sh"
# `starship init bash --print-full-init` prints the whole init script, which is
# static for a given binary: cache it to avoid a process spawn per shell. The
# plain `starship init bash` output is only a 59-byte wrapper that re-forks
# starship when sourced, so the full-init form is what gets cached.
if _starship_bin=$(command -v starship 2>/dev/null); then
  _starship_cache="${XDG_CACHE_HOME:-$HOME/.cache}/starship-init.bash"
  if [ ! -s "$_starship_cache" ] || [ "$_starship_bin" -nt "$_starship_cache" ]; then
    [ -d "${_starship_cache%/*}" ] || mkdir -p "${_starship_cache%/*}"
    # build beside the cache so a broken starship cannot destroy a working one
    if starship init bash --print-full-init > "$_starship_cache.new" 2>/dev/null \
       && [ -s "$_starship_cache.new" ]; then
      mv -f "$_starship_cache.new" "$_starship_cache"
    else
      rm -f "$_starship_cache.new"
    fi
  fi
  . "$_starship_cache"
  unset _starship_bin _starship_cache
fi

# Machine-local overrides (create ~/.env per-machine for secrets/addresses)
[ -f "$HOME/.env" ] && source "$HOME/.env"

# SSH login notification, detached: curl must never delay the prompt, and a
# slow or unreachable host must not hang the shell (hard 5s cap).
if [ -n "$SSH_CONNECTION" ]; then
  (
    curl -s --max-time 5 \
      -H "t:Remote Warning" \
      -d "$(</proc/sys/kernel/hostname): SSH Login Warning
Date: $(date -d '+7 hours' '+%FT%H:%M:%S')
User: $USER
IP Address: ${SSH_CLIENT%% *}
" \
      https://ntfy.sh/whammou-alert >/dev/null 2>&1 &
  )
fi
