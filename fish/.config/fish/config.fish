if status is-interactive
    starship init fish --print-full-init | source
    # colorscript art on startup -- pre-rendered to ~/.cache/colorscripts.
    # The wrapper spends ~70ms in bash before exec'ing the art, and a few
    # palettes (colorbars/print256) need 700/180ms to render live.
    # Rebuild after a colorscripts package update: colorscript-cache -f
    if not set -q NVIM
        set -l cs_cache $HOME/.cache/colorscripts
        test -d $cs_cache; or colorscript-cache
        set -l cs_art (path filter -f $cs_cache/*)
        and cat $cs_art[(random 1 (count $cs_art))]
    end
    abbr --add --global colors 'colorscript --random'
    set fish_greeting
end

function fish_title
    set -q argv[1]; or set argv fish
    echo "FISH | "(pwd)
end

#set fish_cursor_default block
#set fish_cursor_insert line

function ssh --wraps ssh
    if set -q TMUX
        # Extract the target host from SSH arguments
        set -l host
        set -l i 1
        while test $i -le (count $argv)
            set -l a $argv[$i]
            switch $a
                case -[46ACFfgKkNnqTtVvXxY123] # flags without values
                case -[DELOPRSWJbciemop] # flags with one value
                    set i (math $i + 1)
                case --
                    if test $i -lt (count $argv)
                        set host $argv[(math $i + 1)]
                    end
                    break
                case '-*'
                    # unknown flag, skip
                case '*'
                    set host $a
            end
            set i (math $i + 1)
        end
        if set -q host
            # Strip user@ part to get just hostname
            set -l display_host (string split '@' -- $host)[-1]
            tmux rename-window "ssh:$display_host"
            tmux set-environment TMUX_SSH_HOST $display_host
        end
        command ssh $argv
        tmux set-environment -u TMUX_SSH_HOST 2>/dev/null
        tmux set-window-option automatic-rename on 2>/dev/null
    else
        command ssh $argv
    end
end
# Term settings
#export TERM=xterm-256color

# Fish FZF settings
fzf --fish | source

# set Neovim as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"
