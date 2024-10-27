function smb-mount --wraps='sudo mount //171.245.164.181/sambashare /server/ -o username=whammou,password=Unlimitednova199-,uid=1000,uid=1000' --description 'NFS mount'
    sudo mount //116.102.89.170/sambashare /server/ -o username=whammou,password=Unlimitednova199-,uid=1000,uid=1000 $argv && qtile cmd-obj -o widget textbox_1 -f update -a "●   "
        
end
