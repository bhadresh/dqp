"""Find IP Address"""
import os
import socket

if os.name != 'nt':
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
        )[20:24])
    
def get_ip():
    ip = '127.0.0.1'
    if os.name == 'nt': # Windows
        ip = socket.gethostbyname(socket.gethostname())
    else: # *nix
        interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break;
            except IOError:
                pass
    return ip
    
if __name__=="__main__":
    print get_ip()
