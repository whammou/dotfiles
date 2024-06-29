function _paru_install
    set -f listed_packages (
    paru -Slq | 
    _fzf_wrapper \
        --multi \
        --ansi \
        --prompt="AUR> " \
        --preview 'paru -Si {1}'
    )
    if test $status -eq 0
        commandline --replace -- 'paru -S '$listed_packages
    end

commandline --function repaint

end
