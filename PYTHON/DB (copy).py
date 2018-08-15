import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("binding...")
s.bind(('localhost', 3555))

print("listening...")
s.listen(1)

print("accepting...")
conn, addr = s.accept()
print(f"Connection address {addr}" )

while 1:
   print("Receiving...")
   data, addr = s.recvfrom(4)

   if not data: break

   print(f"received data: {data}")
   #s.send(data)
s.close()



