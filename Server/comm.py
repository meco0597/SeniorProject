from UDPserver import *
from Robot import *
import socket
import time

# udp server config
localIP = "192.168.4.1"
udpPort = 5050

firstRobot = Robot(1)
message = firstRobot.robotMessage("Move Forward", 5, 10)
controllerToRobot = {}

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, message)

server = udpServer(udpPort, localIP, messageHandler)

def Main():
    server.startMessageLoop()

if __name__ == '__main__':
    Main()