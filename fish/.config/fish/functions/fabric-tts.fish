function fabric-tts
    pandoc --wrap none -f markdown -t plain | gtts-cli $argv | mpv --force-media-title="Fabric TTS" --no-resume-playback -
end
