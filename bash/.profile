# Login/session environment. Single source of truth: ~/.config/environment.d/*.conf
# — the same files the systemd user manager reads. Nothing is duplicated here.
#
# Import ~/.config/environment.d/*.conf — the systemd user-manager environment —
# so login shells started outside the user manager (TTY, SSH, DM) see the same
# values. The generator is systemd's own parser: do not reimplement its quoting
# or $VAR expansion rules here. Output is newline-separated KEY=VALUE.
# PATH is skipped on purpose: this file builds $PATH below with $HOME expanded.
#
# The generator is a Go binary costing ~6ms per shell, so its output is cached as
# ready-to-source `export` lines in $XDG_CACHE_HOME/envd.sh. The cache is
# rebuilt whenever the generator or any environment.d file is newer than it.
if [ -z "${_ENVD_LOADED:-}" ]; then
  _ENVD_LOADED=1  # deliberately NOT exported: nested login shells must re-read
  _envd_gen=/usr/lib/systemd/user-environment-generators/30-systemd-environment-d-generator
  if [ -x "$_envd_gen" ]; then
    _envd_cache="${XDG_CACHE_HOME:-$HOME/.cache}/envd.sh"
    _envd_stale=
    [ -s "$_envd_cache" ] || _envd_stale=1
    if [ -z "$_envd_stale" ]; then
      for _envd_f in \
        "$_envd_gen" \
        /etc/environment.d/*.conf \
        /usr/lib/environment.d/*.conf \
        "$HOME"/.config/environment.d/*.conf
      do
        if [ "$_envd_f" -nt "$_envd_cache" ]; then
          _envd_stale=1
          break
        fi
      done
    fi
    if [ -n "$_envd_stale" ] && _envd_out=$("$_envd_gen"); then
      [ -d "${_envd_cache%/*}" ] || mkdir -p "${_envd_cache%/*}"
      {
        printf '# generated from systemd environment.d by ~/.profile; do not edit\n'
        while IFS='=' read -r _envd_k _envd_v; do
          [ -n "$_envd_k" ] || continue
          [ "$_envd_k" = PATH ] && continue
          printf 'export %s=%q\n' "$_envd_k" "$_envd_v"
        done <<< "$_envd_out"
      } > "$_envd_cache.$$"
      chmod 600 "$_envd_cache.$$" 2>/dev/null  # may contain secrets from environment.d
      mv -f "$_envd_cache.$$" "$_envd_cache"
    fi
    [ -s "$_envd_cache" ] && . "$_envd_cache"
  fi
  unset _envd_gen _envd_cache _envd_stale _envd_f _envd_out _envd_k _envd_v
fi

# HOME-dependent vars (EnvironmentFile doesn't expand $HOME)
export PATH="$PATH:$HOME/.local/bin:$HOME/.cargo/bin"
export XDG_CONFIG_DIR="$HOME/.config"
export LYNX_CFG_PATH="$HOME/.config/lynx/"
export XAUTHORITY="$HOME/.Xauthority"
