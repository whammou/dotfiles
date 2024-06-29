function fish_user_key_bindings
    fish_vi_key_bindings --no-erase default
    bind --mode default \ci _pacman_install
    bind --mode default \e\ci _paru_install
end

