function smb-umount --wraps='sudo umount -fl /server' --description 'alias smb-umount=sudo umount -fl /server'
  sudo umount -fl /server $argv
        
end
