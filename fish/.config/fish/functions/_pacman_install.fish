function _pacman_install
    set -f listed_packages (
    pacman -Slq | 
    _fzf_wrapper \
        --multi \
        --ansi \
        --prompt="Pacman> " \
        --preview 'pacman -Si {1}'
    )
    if test $status -eq 0
        commandline --replace -- 'sudo pacman -S '$listed_packages
    end

commandline --function repaint

end
