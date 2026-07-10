# Shared environment (flat file — also consumed by systemd services)
set -a
. "$HOME/.config/user-env"
set +a

# HOME-dependent vars (EnvironmentFile doesn't expand $HOME)
export PATH="$PATH:$HOME/.local/bin:$HOME/.cargo/bin"
export XDG_CONFIG_DIR="$HOME/.config"
export LYNX_CFG_PATH="$HOME/.config/lynx/"
