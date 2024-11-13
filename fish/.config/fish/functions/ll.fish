function ll --wraps=ls --wraps='eza -l --icons=always' --description 'alias ll=eza -l'
  eza -l --icons=always $argv
        
end
