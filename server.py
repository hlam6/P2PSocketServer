#Author: Huy Lam
#Client/p2pserver client
#Date: 4/21/2019
#Responsible for file sharing and peer to peer connections
#Run with python 3
from socket import *
import random



class ServerClient:
    #List of connected servers
    current_connections = []
    num_connections = 0
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 15000 + random.randint(1,500)
        self.data=""
        self.neighbor = ""

    def getPeer(self):
        #metaserver port
        print("Client port is ", self.port)
        print("Connecting to metaserver")
        metaserver_port = 12066
        s = socket(AF_INET, SOCK_STREAM)
        host = "127.0.0.1"
        print(host)
        s.connect((host,metaserver_port))
        while True:
            data = input('\nEnter flag here: ')
            print(data)
            s.sendall(data.encode())
            s.sendall(str(self.port).encode()) #send port number

            #Waiting for metaserver to send a referred port number
            serverData = s.recv(4096)
            print(serverData.decode())
            if serverData.decode() == "1":
                print("val is 1")
                return None
            elif serverData.decode() == "Please send valid flag ('P2P')":
                continue
            else:
                print("Closing connection to metaserver")
                s.close()
                print("Data received from server: ", serverData.decode())
                self.connectToReferredServer(serverData.decode())

            #metaserver connection finished
            s.close()
            break
        return serverData.decode()

    def connectToReferredServer(self,serverData):
        #index 0 is port number index 1 is referred port
        commaStrip = serverData.split(',')
        referredPort = commaStrip[1]
        print(commaStrip)
        self.data = commaStrip
        newSocket = socket(AF_INET, SOCK_STREAM)

        newSocket.connect((self.host, int(referredPort)))
        newSocket.sendall("Hello!!".encode())
        newData = newSocket.recv(4096).decode().split(',')
        #Case when referred server has max connections
        if newData[0] == "1":
            newServer = newData[1]
            newSocket.close()
            print("Closing old socket, getting referred")
            newSocket = socket(AF_INET, SOCK_STREAM)
            newSocket.connect((self.host, int(newServer)))
            newSocket.sendall("Hello! Coming from a referral".encode())
            print("Sucessfully connected after referral from peer")
        print("Succesfully connected to referred Server on port ", newSocket.getsockname()[1])
        self.current_connections.append(newSocket.getsockname()[0])
        print("After referral: ",self.current_connections)
        self.num_connections += 1
        return newSocket

    def listenForServer(self):
        print("Listening for other servers...")
        serverPort = self.port
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("", serverPort))
        serverSocket.listen(3)
        while True:
            connectionSocket, addr = serverSocket.accept()
            print("connected to ", addr[0])
            input = connectionSocket.recv(4096).decode()
            print(input)
            self.num_connections += 1
            if self.num_connections > 2:
                self.neighbor = self.current_connections[random.randint(0,1)]
                print("2 Connections is the limit, referring to random neighbor")
                #send 0 if good and 1 and if too many connections
                print("Neighbor port # is ", self.neighbor.getsockname()[1])
                connectionSocket.sendall("1, {}".format(self.neighbor.getsockname()[1]).encode())
            else:
                self.current_connections.append(connectionSocket)
                print("Current connections ", self.current_connections)
                connectionSocket.sendall("0, {}".format(self.neighbor).encode())
        connectionSocket.close()



client = ServerClient()
data = client.getPeer()
client.listenForServer()
