function get-mega-url
    set pwd (pwd | cut -d'/' -f4-)
    set path (string join '' $pwd '/' $argv[1])
    set url (mega-export -a $path | cut -d' ' -f3-)
    echo $url
end
