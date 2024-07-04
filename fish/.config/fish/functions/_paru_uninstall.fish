function _paru_uninstall
    set -f listed_packages (
    paru Qq | 
    _fzf_wrapper \
        --multi \
        --ansi \
        --prompt="Packages> " \
        --preview 'paru -Qi {1}'
    )
    if test $status -eq 0
        commandline --replace -- 'paru -Rncsv '$listed_packages
    end

commandline --function repaint

end
