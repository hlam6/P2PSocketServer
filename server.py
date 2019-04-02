from socket import *

def Main():
    #server ip
    host = "127.0.0.1"
    #server socket port
    port = 12000
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host,port))

    data = input('\nEnter flag here: ')
    s.send(data.encode())
    #Waiting for metaserver to send a referred port number
    serverData = s.recv(4096)
    print("Data received from server: ", serverData.decode())
    referralPort = serverData.decode()[1]
    referralIp = serverData.decode()[0]
    #setup new connection to referred server
    newSocket = socket(AF_INET, SOCK_STREAM)
    newSocket.connect((referralIp, referralPort))
    print("Succesfully connected to referred Server")
