from UDPserver import *
from Robot import *
import socket
import time

# udp server config
localIP = "127.0.0.1"
RobotIP = "192.168.4.7"
multicastIP = '224.0.0.1'
udpPort = 5050
waitTime = 2000

firstRobot = Robot(1)
forwardMessage = firstRobot.robotMessage("Move Forward", 500, 500)
reverseMessage = firstRobot.robotMessage("Move Backward", 500, 500)
stopMessage = firstRobot.robotMessage("Move Forward", 0, 0)

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, forwardMessage)

server = udpServer(udpPort, localIP, messageHandler)

def Main():
    while True:
        #server.sendMessage(forwardMessage, RobotIP, udpPort)
        #time.sleep(waitTime / 1000.0)
        server.sendMessage(reverseMessage, RobotIP, udpPort)
        time.sleep(waitTime / 1000.0)
        server.sendMessage(stopMessage, RobotIP, udpPort)
        time.sleep(waitTime / 1000.0)

if __name__ == '__main__':
    Main()
