function fish_user_key_bindings
    fish_vi_key_bindings default

    for mode in default insert
        bind --mode $mode \e\cp _paru_install
        bind --mode $mode \e\cq _paru_uninstall
        bind --mode $mode \e\co _reset
        bind --mode $mode \co _reset_color
        bind --mode $mode \cg _lazygit

        # bind --mode $mode \cZ true #unbind <C-z> send to background
        # bind --mode $mode \x1c bg

        bind --mode $mode \cf _yazi_current_token
        bind --mode $mode \cs _nvim_current_token
        bind --mode $mode \e\o _bat_preview_current_file
    end
end
