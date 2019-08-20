from Server.UDPserver import *
import Server.WebServer
import socket
import time

# udp server config
localIP = "192.168.4.1"
udpPort = 5005
message = b"Hello ESP"
numOfClients = 2
server = udpServer(udpPort, localIP, messageHandler)

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, b"ACK")


def Main():
    server.startMessageLoop()

#     WebServer.runAsync()
#     while True:
#         currState = WebServer.getState()
#         print(currState)
#         time.sleep(2)



if __name__ == '__main__':
    Main()
