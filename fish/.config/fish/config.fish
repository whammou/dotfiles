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

# FZF settings
#export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#d0d0d0,bg:#000000,hl:#5f87af --color=fg+:#d0d0d0,bg+:#262626,hl+:#00ffff --color=info:#d78700,prompt:#ff005c,pointer:#af5fff --color=marker:#00ff00,spinner:#ae00ff,header:#87afaf"
set fzf_fd_opts --hidden

# PATH
set PATH "/usr/local/bin:$PATH"
set PATH "$HOME/.myscript:$PATH"

# set Nano as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"

# vmux customization
export VMUX_EDITOR=nvim
export VMUX_NVIM_SESSION_DIR=~/.cache/nvim_sessions
export VMUX_GLOBAL=1
export VMUX_NOT_SELECT_PANE=2

# alias for commands:
alias fetch="echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8"
alias yt='ytfzf --detach -c youtube -stl'
alias livetex='mkdir .aux/; latexmk --pvc --auxdir=.aux/ --emulate-aux-dir -recorder- --pdf'
alias grip="grip --render-math --user-content --quiet"
alias tt="tt -theme mine"
alias NOTE="clear; cd /home/whammou/notes; git status"
alias tree="tree -C"
alias scim="sc-im"
alias mdgrep='grep -rin --color=always --include="*.md*"'
alias less="less -R"
alias apt="nala"
alias syncthing="syncthing --no-browser"
alias ls="ls --group-directories-first --sort=extension --color=always"
alias python='python3'
alias calc="python3 -i ~/.myscript/calc.py"
alias rm="rm -i"

export LANG=en_US.UTF-8

