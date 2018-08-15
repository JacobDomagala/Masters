#!/usr/bin/env python

import socket
import json
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5006


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print(f'Connection address: {addr}')
data = json.dumps([40, 20, 20]).encode()

BUFFER_SIZE = sys.getsizeof(data)
print(sys.getsizeof(data))

while 1:
    print(f"sending data: {data}")
    sent = conn.send(data)  # echo
    print(f"Sent {sent} bytes")
    data2 = conn.recv(BUFFER_SIZE)
    if not data2: break
    print(f"received data: {data2}")

conn.close()