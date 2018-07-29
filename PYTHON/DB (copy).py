import socket

socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = "Testowa dane"
sock.sendto(data.encode(), ("10.10.20.40", 3536))


