#Author: Huy Lam
#Course: CSCI4211


from socket import *
from collections import OrderedDict
#for multithreading
from _thread import *
import threading



class ServerConnection:
    numberOfConnections = 0
    #list of ServerConnection objects
    #Used for referring, list of socket objects
    peer_list = []
    #list of ip addresses in order
    ip_list = []
    #peer_cache is an ordered hashmap of servername:# of current connections key-value pairs
    peer_cache = OrderedDict()
    #server_port_dict is an ordered hashmap of servername:port# pairs
    server_port_dict = OrderedDict()
    #Used to advance the peer_list counter for server referral
    nextReferral = 0
    #run with host = "" and port = 12000
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind((self.host,self.port))
        self.firstConnection = True
    def updateConnections(self):
        if self.numberOfConnections < 2:
            self.numberOfConnections += 1
            #if the number of connections is at 2
            if self.numberOfConnections == 2:
                self.nextReferral += 1
        else:
            print("Already at max connections! (2)")
    def addPeer(self, peer):
        #todo: Could add a limit on peers once we reach 2
        self.peer_list.append(peer)
        self.updateConnections()

    #return a message "Port number, Referred port number"
    def getAvailablePeer(self, clientSocket):
        print("in getAvailablePeer")
        servers = list(self.peer_cache.items())
        #Case when available peer has less than 2 connections
        if self.peer_cache[servers[self.nextReferral][0]] < 2:
            #get an available server with less than 2 connections
            availablePeer = (clientSocket.getsockname()[1], self.peer_list[self.nextReferral].getsockname()[1])
            if self.firstConnection:
                self.firstConnection = False
                return availablePeer
            self.peer_cache[servers[self.nextReferral][0]] += 1
            return availablePeer
        #if current peer has 2 connections, go to next item on list
        else:
            self.nextReferral += 1
            availablePeer = (clientSocket.getsockname()[1], self.peer_list[self.nextReferral].getsockname()[1])
            return availablePeer
    #input is a client socket connection
    def handleInput(self, input):
        while True:
            try:
                #2^12 = 4096
                data = input.recv(4096).decode()
                if not data:
                    print("No data received, connection closed (?)\n")
                    #thread_lock.release()
                    break

                if data == "P2P":
                    print("***Valid Flag***")

                    #sends an available server ip to the connected server
                    # if len(serverList) >= 1:
                    #     for server in serverList:
                    #         if server.numberOfConnections == 2:
                    #             continue
                    #         else:
                    #             c = ServerConnection(input.getsockname()[0],input.getsockname()[1])
                    #             c.addPeer(server)
                    #             server.addPeer(c)
                    #             #send client
                    #             input.send("{}, {}".format(input.getsockname()[1], server.getAvailablePeer(input)).encode())
                    #             #input.send("{}, {}".format(input.getsockname()[0], server.getAvailablePeer()).encode())
                    #             print("***Connected to Referred Server ID {}***".format(server.hostName))
                    #
                    #             serverList.append(c)
                    #             break

                    available_peer = self.getAvailablePeer(input)
                    #<port number, referred port number>
                    print("Sending "+"{},{}".format(available_peer[0], available_peer[1]))
                    #print("***Connected to Referred Server ID {}***".format(self.peer_cache[self.nextReferral]))
                    print("***Connected to Referred Server ID " + str(self.ip_list[self.nextReferral]) + "***")
                    print(self.peer_cache)
                    print(self.ip_list)
                    print(self.server_port_dict)
                    input.sendall("{},{}".format(available_peer[0], available_peer[1]).encode())
                    # elif len(serverList) == 0:
                    #     #todo add server to serverList
                    #     newConnection = ServerConnection(input.getsockname()[0], input.getsockname()[1])
                    #     serverList.append(newConnection)
                    print("\n")
                    print("waiting for connections...")

                    break
                else:
                    print("***Invalid Flag***")
                    input.send("Please send valid flag ('P2P')".encode())
            except Exception as e:
                print(e)
                input.close()
                return False

    def run(self):
        self.serverSocket.listen(1)
        print("Waiting for connection\n")
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            self.peer_list.append(connectionSocket)
            self.peer_cache[connectionSocket.getsockname()[0]] = 0
            self.server_port_dict[connectionSocket.getsockname()[0]] = connectionSocket.getsockname()[1]
            self.ip_list.append(connectionSocket.getsockname()[0])
            formatString = '***Connected to {}***'.format(addr[0])
            print(formatString)
            #thread_lock.acquire()
            #start_new_thread(self.handleInput, (connectionSocket,))
            threading.Thread(target = self.handleInput, args = (connectionSocket,)).start()
        input.close()
## IMPORTANT GLOBALS ##

#thread_lock = threading.lock()

#def Main():
    #sock.getsockname()[1] to get port

Server = ServerConnection("", 12020)
Server.run()
