# Login/session environment. Single source of truth: ~/.config/environment.d/*.conf
# — the same files the systemd user manager reads. Nothing is duplicated here.
#
# Import ~/.config/environment.d/*.conf — the systemd user-manager environment —
# so login shells started outside the user manager (TTY, SSH, DM) see the same
# values. The generator is systemd's own parser: do not reimplement its quoting
# or $VAR expansion rules here. Output is newline-separated KEY=VALUE.
# PATH is skipped on purpose: this file builds $PATH below with $HOME expanded.
if [ -z "${_ENVD_LOADED:-}" ]; then
  _ENVD_LOADED=1  # deliberately NOT exported: nested login shells must re-read
  _envd_gen=/usr/lib/systemd/user-environment-generators/30-systemd-environment-d-generator
  if [ -x "$_envd_gen" ]; then
    while IFS='=' read -r _k _v || [ -n "$_k" ]; do
      [ -n "$_k" ] || continue
      [ "$_k" = PATH ] && continue
      export "$_k=$_v"
    done < <("$_envd_gen")
  fi
  unset _envd_gen _k _v
fi

# HOME-dependent vars (EnvironmentFile doesn't expand $HOME)
export PATH="$PATH:$HOME/.local/bin:$HOME/.cargo/bin"
export XDG_CONFIG_DIR="$HOME/.config"
export LYNX_CFG_PATH="$HOME/.config/lynx/"
export XAUTHORITY="$HOME/.Xauthority"
