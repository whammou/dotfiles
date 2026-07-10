#!/usr/bin/env bash
set -euo pipefail

DOTFILES="$(cd "$(dirname "$0")" && pwd)"

echo "==> Installing theme packages..."
sudo pacman -S --needed \
  kvantum \
  papirus-icon-theme \
  qt5ct \
  qt6ct

# adw-gtk3 from AUR — provides the base widget CSS for both GTK3 and GTK4
# Color overrides come from our gtk.css in the gtk/ stow package
if ! pacman -Qi adw-gtk3 &>/dev/null; then
  echo "==> Installing adw-gtk3 (AUR)..."
  yay -S --needed adw-gtk3 2>/dev/null || paru -S --needed adw-gtk3 2>/dev/null || {
    echo "WARNING: Install adw-gtk3 manually from AUR"
  }
fi

# Stow all packages
echo "==> Stowing dotfiles..."
cd "$DOTFILES"
for pkg in bash gtk qt kvantum; do
  echo "  stow $pkg..."
  stow -R "$pkg" 2>/dev/null && echo "    done" || echo "    skipped (already exists?)"
done

echo ""
echo "==> Done! Restart your session or source ~/.bashrc"
echo "==> For Firefox: install 'One Dark Pro' theme from addons.mozilla.org"
echo "==> For LibreOffice: configure tools → options → view → icon theme = Papirus"
