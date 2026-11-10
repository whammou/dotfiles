function colorscript-cache --description 'Pre-render colorscripts to ~/.cache/colorscripts (the colorscript wrapper costs ~70ms)'
    argparse 'f/force' -- $argv; or return

    set -l src /opt/shell-color-scripts/colorscripts
    set -l dst $HOME/.cache/colorscripts

    for f in (path filter -f $src/*)
        set -l name (string replace -r '^.*/' '' -- $f)
        if test -s $dst/$name; and not set -q _flag_force
            continue
        end
        mkdir -p $dst
        $f >$dst/$name 2>/dev/null
    end

    for f in $dst/*
        test -s $f; or rm -f $f
    end
end
