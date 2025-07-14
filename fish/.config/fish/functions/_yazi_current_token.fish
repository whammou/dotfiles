function _yazi_current_token -d "List contents of token under the cursor if it is a directory, otherwise list the contents of the current directory"
    set -l val "$(commandline -t | string replace -r '^~' "$HOME")"
    set -l cmd
    if test -d $val
        set cmd _yazi $val
    else
        set -l dir (dirname -- $val)
        if test $dir != . -a -d $dir
            set cmd _yazi $dir
        else
            set cmd _yazi
        end
    end
    __fish_echo $cmd
    commandline -f repaint
end
