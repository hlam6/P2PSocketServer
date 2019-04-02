#Author: Huy Lam
#Course: CSCI4211


from socket import *

#for multithreading
from _thread import *
import threading



class ServerConnection:
    numberOfConnections = 0
    #list of ServerConnection objects
    peer_list = []
    def __init__(self, host, port):
        self.hostName = host
        self.port = port
    def updateConnections(self):
        if self.numberOfConnections < 2:
            self.numberOfConnections+=1
        else:
            print("Already at max connections! (2)")
    def addPeer(self, peer):
        #todo: Could add a limit on peers once we reach 2
        self.peer_list.append(peer)
        self.updateConnections()
    def getAvailablePeer(self):
        formatStr = "" + peer_list[0].hostName + ", " + peer_list[0].port
        referredPort = peer_list[0].port
        return self.port


## IMPORTANT GLOBALS ##

#thread_lock = threading.lock()
#server cache is a hashmap of servername:# of current connections key-value pairs
#list is used to maintain server names in the order they were connected, which dictionaries do not.
serverList = []
serverCache = {}

#input is a client socket connection
def handleInput(input):
    while True:
        #2^12 = 4096
        data = input.recv(4096).decode()
        if not data:
            print("No data received, connection closed (?)\n")

            #thread_lock.release()
            break

        if data == "P2P":
            print("***Valid Flag***")

            #sends an available server ip to the connected server
            if len(serverList) >= 1:
                for server in serverList:
                    if server.numberOfConnections == 2:
                        continue
                    else:
                        c = ServerConnection(input.getsockname()[0],input.getsockname()[1])
                        c.addPeer(server)
                        server.addPeer(c)
                        #send client
                        input.send("{}, {}".format(input.getsockname()[1], server.getAvailablePeer()).encode())
                        #input.send("{}, {}".format(input.getsockname()[0], server.getAvailablePeer()).encode())
                        print("***Connected to Referred Server ID {}***".format(server.hostName))

                        serverList.append(c)
                        break
            elif len(serverList) == 0:
                #todo add server to serverList
                newConnection = ServerConnection(input.getsockname()[0], input.getsockname()[1])
                serverList.append(newConnection)

            input.close()
        else:
            print("***Invalid Flag***")
            input.send("Please send valid flag".encode())



serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("Waiting for connection\n")

while True:
    connectionSocket, addr = serverSocket.accept()
    formatString = '***Connected to {}***'.format(addr[0])
    print(formatString)
    #thread_lock.acquire()
    start_new_thread(handleInput, (connectionSocket,))
serverSocket.close()
