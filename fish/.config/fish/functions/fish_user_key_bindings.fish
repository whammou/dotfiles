function fish_user_key_bindings
    fish_vi_key_bindings default

    for mode in default insert
        bind --mode $mode \e\cp _paru_install
        bind --mode $mode \e\cq _paru_uninstall
        bind --mode $mode \co _reset
        bind --mode $mode \cg fug

        bind --mode $mode \cZ true #unbind <C-z> send to background
        bind --mode $mode \x1c bg
    end
end

