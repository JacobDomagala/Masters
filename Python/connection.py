import socket
import json

class TcpClient:
    def __init__(self):
        self.m_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_Conn = 0
        self.m_Addr = 0
        self.m_Bound = False
    
    def BindTo(self, address):
        if not self.m_Bound:
            print("Waiting for Matlab to connect...")
            self.m_Socket.bind(address)
            self.m_Socket.listen(1)

            self.m_Conn, self.m_Addr = self.m_Socket.accept()
            print("Matlab connected! Address" + str(self.m_Addr))
            self.m_Bound = True

    def Disconnect(self):
        self.m_Socket.close()

    def SendData(self, data):
        return self.m_Conn.send(json.dumps(data).encode())

    def RecvData(self, bytesToRead = 8, timeoutInSeconds = 1):
        try:
           self.m_Conn.settimeout(timeoutInSeconds)
           rawData = self.m_Conn.recv(bytesToRead).decode()
           print("Data received! " + str(rawData))
           return json.loads(rawData)
        except:
            print("Timeout while receiving data from Matlab!")
            return [0,0]

