from Server.UDPserver import *
from WiiController.wiiScale import *
from Server.Robot import *
import socket
import time

# udp server config
localIP = "127.0.0.1"
RobotIP = "192.168.4.6"
RobotIP2 = "192.168.4.15"
RobotIP3 = "192.168.4.13"
RobotIP4 = "192.168.4.18"
multicastIP = '224.0.0.1'
udpPort = 5050
waitTime = 2000
motorSpeed = 1023

robotCommands = RobotCommand(1)
forwardMessage = robotCommands.robotMessage("Move Forward", motorSpeed, motorSpeed)
reverseMessage = robotCommands.robotMessage("Move Backward", motorSpeed, motorSpeed)
stopMessage = robotCommands.robotMessage("Move Forward", 0, 0)

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, forwardMessage)

server = udpServer(udpPort, localIP, messageHandler)

def getCommand(values, weightDifferential):
    frontLeft = values[0]
    frontRight = values[1]
    backLeft = values[2]
    backRight = values[3]
    frontAverage = (frontLeft + frontRight) / 2
    backAverage = (backLeft + backRight) / 2
    leftAverage = (frontLeft + backLeft) / 2
    rightAverage = (frontRight + backRight) / 2
    if frontAverage - backAverage > weightDifferential:
        return robotCommands.robotMessage("Move Forward", motorSpeed, motorSpeed)
    elif backAverage - frontAverage > weightDifferential:
        return robotCommands.robotMessage("Move Backward", motorSpeed, motorSpeed)
    elif rightAverage - leftAverage > weightDifferential:
        return robotCommands.robotMessage("Rotate Right", motorSpeed, motorSpeed)
    elif leftAverage - rightAverage > weightDifferential:
        return robotCommands.robotMessage("Rotate Left", motorSpeed, motorSpeed)
    else:
        return robotCommands.robotMessage("Move Forward", 0, 0)
    

def Main():
    #address1 = "00:22:4C:69:01:27"
    #address2 = "00:24:1E:FC:18:65"
    #address3 = "00:1F:C5:A8:81:55"
    #address4 = "00:1F:C5:A7:DF:6C"
    #controller = WiiController()
    #controller.start(address1)
    #controller.start(address2)
    #controller.start(address3)
    #controller.start(address4)
    #while True:
        #userInput = controller.get_data(address1)
        #userInput2 = controller.get_data(address2)
        #userInput3 = controller.get_data(address3)
        #userInput4 = controller.get_data(address4)
        #server.sendMessage(getCommand(userInput, 15), RobotIP, udpPort)
        #server.sendMessage(getCommand(userInput2, 15), RobotIP2, udpPort)
        #server.sendMessage(getCommand(userInput3, 15), RobotIP3, udpPort)
        #server.sendMessage(getCommand(userInput4, 15), RobotIP4, udpPort)
        #time.sleep(0.1)
        server.sendMessage(forwardMessage, RobotIP4, udpPort)
        time.sleep(waitTime / 1000.0)
        #server.sendMessage(reverseMessage, RobotIP, udpPort)
        #time.sleep(waitTime / 1000.0)
        server.sendMessage(stopMessage, RobotIP4, udpPort)
        #server.sendMessage(stopMessage, RobotIP2, udpPort)
        time.sleep(waitTime / 1000.0)

if __name__ == '__main__':
    Main()
