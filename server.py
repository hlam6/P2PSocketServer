#Author: Huy Lam
#Client/p2pserver client
#Run with python 3
from socket import *





#server socket port
port = 12020
s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
print(host)
s.connect((host,port))
while True:
    data = input('\nEnter flag here: ')
    print(data)
    s.send(data.encode())
    #Waiting for metaserver to send a referred port number
    serverData = s.recv(4096)
    print("Data received from server: ", serverData.decode())
    referralPort = serverData.decode()
    referralIp = serverData.decode()
    #metaserver connection finished
s.close()
#setup new connection to referred server
newSocket = socket(AF_INET, SOCK_STREAM)
newSocket.connect((referralIp, referralPort))
print("Succesfully connected to referred Server")
