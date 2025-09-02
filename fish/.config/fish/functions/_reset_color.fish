function _reset_color
    reset
    if not set -q NVIM
        echo
        #fastfetch
        colorscript --random
        echo \n
    end
    commandline --function repaint
end
