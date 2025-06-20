if status is-interactive

    # Commands to run in interactive sessions can go here
    starship init fish | source
    # echo; neofetch --ascii_distro arch_small --ascii_colors 6 6 --colors 5 8 10 6 8 8
    echo
    #fastfetch
    colorscript --random
    set fish_greeting

    #    if string match -q -- '*' $TERM
    #        set -g fish_vi_force_cursor 1
    #    end
end
function fish_title
    set -q argv[1]; or set argv fish
    set -l current_path_abbreviated (fish_prompt_pwd_dir_length=1 prompt_pwd)
    set -l current_path_expanded (string replace '~' "HOME" -- "$current_path_abbreviated")
    echo "$current_path_expanded - "
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
