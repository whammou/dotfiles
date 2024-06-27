function odtkular
    set file (path basename $argv[1] | string split -r -m1 .)[1]
    set pdf (string join '' $file .pdf)
    libreoffice --convert-to pdf $argv[1] --outdir /tmp/
    okular /tmp/$pdf
end
