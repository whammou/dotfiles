if status is-interactive
    # Commands to run in interactive sessions can go here
    starship init fish | source
    # echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8
    echo; fastfetch
    set fish_greeting
    if string match -q -- 'tmux*' $TERM
        set -g fish_vi_force_cursor 1
    end
end
set fish_cursor_default block
set fish_cursor_insert line

# Term settings
export TERM=xterm-256color

# Fish FZF settings
set fzf_fd_opts --hidden

# set Neovim as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"

# vmux customization
export VMUX_EDITOR=nvim
export VMUX_NVIM_SESSION_DIR=~/.cache/nvim_sessions
export VMUX_GLOBAL=1
export VMUX_NOT_SELECT_PANE=2

# fzf source
export FZF_DEFAULT_OPTS_FILE=$HOME/.config/fzf/config

# alias for commands:
#alias livetex='mkdir .aux/; latexmk --pvc --auxdir=.aux/ --emulate-aux-dir -recorder- --pdf'
#export LANG=en_US.UTF-8

