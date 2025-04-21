if status is-interactive

    # Commands to run in interactive sessions can go here
    starship init fish | source
    # echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8
    echo
    fastfetch
    set fish_greeting

    #    if string match -q -- '*' $TERM
    #        set -g fish_vi_force_cursor 1
    #    end
end

#set fish_cursor_default block
#set fish_cursor_insert line

# Term settings
#export TERM=xterm-256color

# Fish FZF settings
fzf --fish | source

# set Neovim as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"
