if status is-interactive
    # Commands to run in interactive sessions can go here
    clear -x
    echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8
    starship init fish | source
    set fish_greeting
end

function fish_user_key_bindings
    fish_vi_key_bindings --no-erase default
end

if status is-interactive
    if string match -q -- 'tmux*' $TERM
        set -g fish_vi_force_cursor 1
    end
end

set fish_cursor_default block
set fish_cursor_insert line

function goto
    vmux $argv[1] "+$argv[2]" -c "normal zo"
end

function odtkular
    set file (path basename $argv[1] | string split -r -m1 .)[1]
    set pdf (string join '' $file .pdf)
    libreoffice --convert-to pdf $argv[1] --outdir /tmp/
    okular /tmp/$pdf
end

function get-mega-url
    set pwd (pwd | cut -d'/' -f4-)
    set path (string join '' $pwd '/' $argv[1])
    set url (mega-export -a $path | cut -d' ' -f3-)
    echo $url
end

export TERM=xterm-256color
export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#d0d0d0,bg:#000000,hl:#5f87af --color=fg+:#d0d0d0,bg+:#262626,hl+:#00ffff --color=info:#d78700,prompt:#ff005c,pointer:#af5fff --color=marker:#00ff00,spinner:#ae00ff,header:#87afaf"

# PATH
export PATH="$PATH:/usr/lib/python3/dist-packages/stubtest"
export PATH="$PATH:/opt/nvim"
set PATH "$HOME/.local/bin:$PATH"
set PATH "$HOME/.cargo/bin:$PATH"
set PATH "/opt/nvim:$PATH"

set PATH "$HOME/.myscript:$PATH"
set PATH "/usr/lib/vktablet/:$PATH"

# set Nano as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"
# vmux customization
export VMUX_EDITOR=nvim
#export VMUX_REALEDITOR_NVIM=/usr/local/bin/nvim
export VMUX_NVIM_SESSION_DIR=~/.cache/nvim_sessions
export VMUX_GLOBAL=1
export VMUX_NOT_SELECT_PANE=2

# alias for commands:
alias fetch="echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8"
alias yt='ytfzf --detach -c youtube -stl'
alias livetex='mkdir .aux/; latexmk --pvc --auxdir=.aux/ --emulate-aux-dir -recorder- --pdf'
alias cat='ccat -G String="teal" -G Plaintext="darkgray" -G Keyword="turquoise" -G Decimal="red" -G Type="fuchsia" -G Punctuation="green"'
alias shellgpt="bash && cd ~/shellgpt/; source shellgpt/bin/activate; clear"
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

export LANG=en_US.UTF-8

