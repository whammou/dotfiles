function ttsmd
    pandoc --wrap none -f markdown -t plain | gtts-cli $argv | mpv -
end
