#Author: Huy Lam
#Course: CSCI4211
#Date: 4/21/2019

from socket import *
from collections import OrderedDict
#for multithreading
from _thread import *
import threading
import random


class ServerConnection:
    numberOfConnections = 0
    #list of ServerConnection objects
    #Used for referring, list of socket objects
    peer_list = []
    #list of ip addresses in order
    ip_list = []
    port_list = []
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
        self.nextPort = self.port + random.randint(10,200)

    #Refer server to first item in peer cache
    #return a message "Port number, Referred port number"
    def getAvailablePeer(self, clientSocket):
        print("in getAvailablePeer")
        servers = list(self.peer_cache.items())
        print(servers)

        return self.peer_list[0]
    #input is a client socket connection
    def handleInput(self, input):
        while True:
            try:
                #2^12 = 4096
                data = input.recv(4096).decode()
                if not data:
                    print("No data received, connection closed (?)\n")

                    break

                if data == "P2P":
                    print("***Valid Flag***")
                    #get port #
                    data = input.recv(4096).decode()
                    self.port_list.append(data)
                    print(data)
                    if self.firstConnection:
                        print("Adding first server")
                        self.firstConnection = False
                        input.sendall("1".encode())
                        break
                    available_peer = self.getAvailablePeer(input)
                    print("Finished with getAvailablePeer")
                    #<port number, referred port number>
                    print("***Connected to Referred Server ID " + str(self.ip_list[self.nextReferral]) + "***")
                    print(self.peer_cache)
                    print(self.ip_list)
                    print(self.server_port_dict)
                    print(self.port_list)
                    print(input.getsockname()[1])
                #    input.sendall("{},{}".format(input.getsockname()[1], available_peer.getsockname()[1]).encode())
                    input.sendall("{},{}".format(input.getsockname()[1], self.port_list[0]).encode())
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
        print("Closing connection to ", input)
        input.close()

Server = ServerConnection("", 12066)
Server.run()
