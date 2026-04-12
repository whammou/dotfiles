if status is-interactive
    starship init fish | source
    echo
    if not set -q NVIM
        colorscript --random
    end
    set fish_greeting
end

function fish_title
    set -q argv[1]; or set argv fish
    echo (pwd)" - "
end

#set fish_cursor_default block
#set fish_cursor_insert line

#function ssh
#    if set -q $TMUX
#        tmux rename-window (echo $argv | cut -d . -f 1)
#        command ssh "$argv"
#        tmux set-window-option automatic-rename on 1>/dev/null
#    else
#        command ssh "$argv"
#    end
#end
# Term settings
#export TERM=xterm-256color

# Fish FZF settings
fzf --fish | source

# set Neovim as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"
