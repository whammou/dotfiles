function fug --wraps=nvim\ +\':G\ \|\ only\' --description alias\ fug=nvim\ +\':G\ \|\ only\'
  nvim +':G | only' $argv
        
end
