import socket

while 1:
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   data = "Testowa dane"
   sock.sendto(data.encode(), ("10.10.20.82", 4012))


