function fabric-read
    cat .input.org | pandoc --wrap=none -f org -t markdown -
end
