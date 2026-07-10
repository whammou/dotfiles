#!/usr/bin/env bash

# ==============================================================
# Terminal fzf config that mimics fzf-lua + LazyVim defaults
# ==============================================================
# How fzf-lua maps Neovim highlights → fzf colors:
#
#   fzf-lua flag     Neovim hl group       Links to
#   ─────────────────────────────────────────────────────
#   fg               FzfLuaFzfNormal       → Normal         (terminal default)
#   bg               FzfLuaFzfNormal       → Normal         (terminal default)
#   hl               FzfLuaFzfMatch        → Special        (yellow/magenta)
#   fg+/bg+          FzfLuaFzfCursorLine   → CursorLine     (highlighted line)
#   hl+              FzfLuaFzfMatch        → Special
#   info             FzfLuaFzfInfo         → NonText        (dim)
#   prompt/pointer   FzfLuaFzfPrompt/Pointer → Special
#   query            FzfLuaFzfQuery        → Normal, regular weight
#   border/separator FzfLuaFzfBorder       → Normal
#   gutter           FzfLuaFzfGutter       → Normal
#
# The numbers below (3=yellow, 5=magenta, 8=bright black)
# are ANSI terminal color codes that approximate how a
# typical dark Neovim theme would render: Special=yellow,
# NonText=gray, CursorLine=slightly lighter bg, etc.

export FZF_DEFAULT_OPTS="
  --layout=reverse
  --info=inline-right
  --highlight-line
  --no-scrollbar
  --border=sharp
  --input-border=none
  --list-border=none
  --preview-border=none
  --preview-label-pos=0
  --list-border=none
  --header-border=none
  --footer-border=none
  --ansi
  --color=fg:-1,bg:-1,hl:1,fg+:-1,bg+:8,hl+:1
  --color=info:15,prompt:4,pointer:1,marker:1,spinner:1
  --color=header:-1,separator:15,scrollbar:-1,border:15
  --color=query:-1:regular
  --pointer='▌'
  --marker='▌'
  --bind='ctrl-z:abort'
  --bind='ctrl-u:half-page-up'
  --bind='ctrl-d:half-page-down'
  --bind='ctrl-x:jump'
  --bind='ctrl-f:preview-page-down'
  --bind='ctrl-b:preview-page-up'
  --bind='ctrl-q:select-all+accept'
  --bind='ctrl-a:beginning-of-line'
  --bind='ctrl-e:end-of-line'
  --bind='alt-a:toggle-all'
  --bind='alt-g:first,alt-G:last'
  --bind='f3:toggle-preview-wrap'
  --bind='f4:toggle-preview'
  --bind='shift-down:preview-page-down,shift-up:preview-page-up'
  --bind='alt-shift-down:preview-down,alt-shift-up:preview-up'
"

# ── Preview window defaults (matches fzf-lua's flex layout) ──────────
# fzf-lua defaults:
#   vertical   = "down:45%"
#   horizontal = "right:60%"
#   layout     = "flex"       (flip at 100 cols)
#   border     = "rounded"
#   wrap       = false
#   hidden     = false
export FZF_DEFAULT_OPTS="
  $FZF_DEFAULT_OPTS
  --preview-window='right:60%:nohidden:nowrap:border-line'
"

# ── Per-command wrappers ────────────────────────────────────────────
# fzf-lua has different configs per picker (files, grep, buffers, etc).
# These shell functions use the same external commands fzf-lua uses.

# Default previewer - uses bat like fzf-lua's builtin/bat previewer
# fzf-lua: bat --color=always --style=numbers,changes {}
_fzf_preview_bat() {
  bat --color=always --style=numbers,changes --highlight-line {} 2>/dev/null
}

# fzf-lua "files" picker equivalent
# fzf-lua defaults: fd --color=never --type f --type l --exclude .git --exclude .jj
fzl-files() {
  local fd_cmd="fd --color=never --type f --type l --exclude .git --exclude .jj"
  eval "$fd_cmd" | fzf \
    --prompt='Files> ' \
    --scheme=path \
    --multi \
    --preview="_fzf_preview_bat" \
    --header='ctrl-s:split | ctrl-v:vsplit | ctrl-t:tab | alt-.:toggle-root' \
    "$@"
}

# fzf-lua "git_files" picker equivalent
fzl-git-files() {
  git ls-files --exclude-standard --cached --others 2>/dev/null | fzf \
    --prompt='Git Files> ' \
    --scheme=path \
    --multi \
    --preview="_fzf_preview_bat" \
    "$@"
}

# fzf-lua "live_grep" / "grep" picker equivalent
# fzf-lua defaults: rg --column --line-number --no-heading --color=always --smart-case
fzl-grep() {
  local query="$1"
  if [[ -z "$query" ]]; then
    echo "Usage: fzl-grep <pattern>"
    return 1
  fi
  rg --column --line-number --no-heading --color=always --smart-case \
    --max-columns=4096 "$query" 2>/dev/null | fzf \
    --prompt='Grep> ' \
    --multi \
    --delimiter='[:]' \
    --with-nth='2..' \
    --nth='2..' \
    --preview='bat --color=always --style=numbers --highlight-line {1}' \
    --preview-window='+{2}/3:nowrap' \
    --header='ctrl-s:split | ctrl-v:vsplit | ctrl-t:tab' \
    "$@"
}

# fzf-lua "buffers" picker equivalent
fzl-buffers() {
  # If inside Neovim, use fzf-lua's buffers instead
  if [[ -n "$NVIM" ]] || [[ -n "$VIM_TERMINAL" ]]; then
    nvim +":FzfLua buffers" </dev/tty
    return
  fi
  echo "Run inside Neovim for buffers, or use:"
  echo "  ps aux | fzf   (for processes)"
  echo "  fzl-files       (for files)"
}

# fzf-lua "oldfiles" equivalent (uses $HISTFILE)
fzl-recent() {
  # Show recently edited files from the current directory (last 50)
  if command -v zoxide &>/dev/null; then
    zoxide query -l | head -50 | fzf \
      --prompt='Recent> ' \
      --preview="_fzf_preview_bat" \
      "$@"
  else
    echo "Install zoxide for recent files tracking"
    return 1
  fi
}

# fzf-lua global picker (files + grep combined)
# This is a simplified version of fzf-lua's "global" picker
fzl() {
  if [[ "$#" -eq 0 ]]; then
    fzl-files
  else
    fzl-grep "$*"
  fi
}
