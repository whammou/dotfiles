function fabric-view
    pandoc --wrap=none -f markdown -t org - \
        | nvim -c "setfiletype org" +"set wrap" +"set spell" \
        -c "0read ~/.input.org" \
        -c "lua vim.fn.system([[ \
  curl \
  -H t:Gemini' \
  -d 'Output is ready' \
  ntfy.sh/whammou_alert \
  ]])"
end
