function notes --wraps='cd notes && git fetch' --wraps='cd ~/notes && git fetch' --description 'Open Notes and fetch update'
  cd ~/notes && git fetch $argv
        
end
