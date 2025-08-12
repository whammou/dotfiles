function fabric-view
    pandoc --wrap=none -f markdown -t org - | nvim -c "setfiletype org" -c "set wrap" -c "0read ~/.input.org" -c "lua vim.fn.system([[notify-send -u low 'Gemini' 'Output is ready']])"
end
