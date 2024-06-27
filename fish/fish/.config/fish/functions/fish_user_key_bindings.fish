function fish_user_key_bindings
    fish_vi_key_bindings --no-erase default
    bind --mode default \e\cu _pacman_install
end

