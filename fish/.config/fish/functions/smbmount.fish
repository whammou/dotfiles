function smbmount
    set port $argv[1]
    sudo mount -t cifs //0.tcp.ap.ngrok.io/sambashare ~/server -o username=whammou,password=Unlimitednova199-,uid=1000,gid=1000,workgroup=workgroup,mfsymlinks,port=$port
end
