function fish_user_key_bindings
    fish_vi_key_bindings default

    for mode in default insert
        bind --mode $mode \cs _paru_install
        bind --mode $mode \e\cq _paru_uninstall
        bind --mode $mode \co _reset
    end
end

