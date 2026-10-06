function _baleia_yank --description "Open terminal scrollback in nvim+baleia to yank lines"
    set -l tmp (mktemp /tmp/fish-scrollback.XXXXXX)
    or return 1

    if set -q TMUX
        tmux capture-pane -e -p -J -S -3000 >$tmp
    else if set -q KITTY_PID
        kitty @ get-text --ansi --extent=all >$tmp
    else
        echo "baleia-yank: no TMUX or KITTY_PID detected, cannot capture scrollback" >&2
        rm -f $tmp
        return 1
    end

    # Strip OSC sequences (shell-integration markers like 133;A, hyperlinks):
    # kitty/tmux capture keeps SGR colors for baleia but leaves OSC markers
    # behind in various shapes (full ESC ] … ST, or bare ]133;A\ residue)
    # that baleia won't touch. The [^space]* tails catch any terminator.
    sed -i -e 's/\x1b\][^\x07\x1b]*\(\x07\|\x1b\\\)//g' -e 's/\]133;[^[:space:]]*//g' -e 's/\]8;;[^[:space:]]*//g' $tmp

    if not test -s $tmp
        echo "baleia-yank: empty scrollback capture" >&2
        rm -f $tmp
        return 1
    end

    nvim -c "BaleiaColorize" -c "set nomodified" $tmp
    rm -f $tmp
    commandline -f repaint
end
