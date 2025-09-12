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
    set -l current_path_abbreviated (fish_prompt_pwd_dir_length=1 prompt_pwd)
    set -l current_path_expanded (string replace '~' "HOME" -- "$current_path_abbreviated")
    echo "$current_path_expanded - "
end
set fish_cursor_default block
set fish_cursor_insert line

# Term settings
#export TERM=xterm-256color

# Fish FZF settings
fzf --fish | source

# set Neovim as default text editor
export VISUAL=nvim
export EDITOR="$VISUAL"
