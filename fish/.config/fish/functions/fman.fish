function fman --description "Fuzzy-find and preview man pages"
    set -l query ""
    if set -q argv[1]
        set query $argv[1]
    end

    man -k . | fzf -q $query --prompt='man> ' \
        --preview "echo {} | tr -d '()' | awk '{printf \"%s \", \$2} {print \$1}' | xargs -r man 2>/dev/null | col -bx | bat -l man -p --color always" |
        tr -d '()' | awk '{printf "%s ", $2} {print $1}' | xargs -r man 2>/dev/null
    commandline --function repaint
end
