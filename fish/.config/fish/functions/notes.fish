function notes --wraps='cd notes && git fetch' --wraps='cd ~/notes && git fetch' --description 'alias notes=cd ~/notes && git fetch'
  cd ~/notes && git fetch $argv
        
end
