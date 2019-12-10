from Server.UDPserver import *
from Server.Robot import *
from OpenCV.colorDetectionWebCamera import *
from WiiController.wiiScale import *
import socket
import time
import threading 
import sys

# udp server config
localIP = "127.0.0.1"
udpPort = 5050
motorSpeed = 1023
gamemode = "ffa"

# color ranges config
colorRanges = {
    'Red': [([0, 150, 50], [10, 255, 255]), ([170, 150, 50], [180, 255, 255])],
    'Green': [([30, 40, 5], [90, 255, 255])],
    'Blue': [([100, 40, 5], [130, 255, 255])],
    'Yellow': [([20, 40, 40], [35, 255, 255])]
}
colorDetection = ColorDetectionWebCamera(colorRanges, _threshold=500, _show=True)

# wiiboard config
controllerAddresses = {
    'Red': "00:22:4C:69:01:27",
    'Green': "00:24:1E:FC:18:65",
    'Blue': "00:1F:C5:A8:81:55",
    'Yellow': "00:1F:C5:A7:DF:6C"
}
controllers = WiiController()

# robot config
robotIPs = {
    'Red': "192.168.4.15",
    'Green': "192.168.4.18",
    'Blue': "192.168.4.13",
    'Yellow': "192.168.4.6"
}
robotCommands = RobotCommand()

# server initialization
def messageHandler(data, addr):
    print(data, addr)

server = udpServer(udpPort, localIP, messageHandler)

def isWeightOnController(color):
    weightSum = 0
    values = controllers.get_data(controllerAddresses[color])
    weightSum += values[0]
    weightSum += values[1]
    weightSum += values[2]
    weightSum += values[3]
    if weightSum >= 20:
        return True
    else:
        return False

def getCommand(values):
    frontLeft = values[0]
    frontRight = values[1]
    backLeft = values[2]
    backRight = values[3]
    frontAverage = (frontLeft + frontRight) / 2
    backAverage = (backLeft + backRight) / 2
    leftAverage = (frontLeft + backLeft) / 2
    rightAverage = (frontRight + backRight) / 2
    if rightAverage - leftAverage > 10:
        return robotCommands.robotMessage("Rotate Right", motorSpeed, motorSpeed)
    elif leftAverage - rightAverage > 10:
        return robotCommands.robotMessage("Rotate Left", motorSpeed, motorSpeed)
    elif frontAverage - backAverage > 10:
        return robotCommands.robotMessage("Move Forward", motorSpeed, motorSpeed)
    elif backAverage - frontAverage > 10:
        return robotCommands.robotMessage("Move Backward", motorSpeed, motorSpeed)
    else:
        return robotCommands.robotMessage("Move Forward", 0, 0)


def Main():
    #game state varible
    gameState = "setup"
    # fire up the wii boards
    for key in controllerAddresses:
        controllers.start(controllerAddresses[key])
    # fire up the color detection thread
    detectionThread = threading.Thread(target=colorDetection.startDetection)
    detectionThread.start()

    spinMessage = robotCommands.robotMessage("Rotate Right", 1000, 1000)
    stopMessage = robotCommands.robotMessage("Move Forward", 0, 0)
    playersLeft = []
    ffa = False
    # main loop
    while True:
        try:
            time.sleep(0.05)
        except (KeyboardInterrupt, SystemExit):
            colorDetection.running = False
            detectionThread.join()
            sys.exit()
        # keeps the controllers alive
        if gameState != "gameLoop":
            for controller in controllerAddresses:
                userInput = controllers.get_data(controllerAddresses[controller])
        # configure the game
        if gameState == "setup":
            gameState = "countdown"

            if gamemode == "ffa":
                playersLeft = []
                for color in colorRanges:
                    if (colorDetection.isDetected(color) == True and isWeightOnController(color) == False) or (colorDetection.isDetected(color) == False and isWeightOnController(color) == True):
                        gameState = "setup"
                        if color in playersLeft:
                            playersLeft.remove(color)
                    if (colorDetection.isDetected(color) == True and isWeightOnController(color) == True):
                        if color not in playersLeft:
                            playersLeft.append(color)
                if (len(playersLeft) < 2):
                    gameState = "setup"
                    
            elif gamemode == "team":
                playersLeft = ["Red", "Blue", "Green", "Yellow"]
                for color in colorRanges:
                    if (colorDetection.isDetected(color) == False or isWeightOnController(color) == False):
                        gameState = "setup"

            time.sleep(1)
        # countdown state
        elif gameState == "countdown":          
            for robot in playersLeft:
                server.sendMessage(spinMessage, robotIPs[robot], udpPort)
            time.sleep(2)
            gameState = "gameLoop"
        # main game loop
        elif gameState == "gameLoop":
            # we have a winner
            if gamemode == "ffa":
                if len(playersLeft) == 1:
                    gameState = "setup"
                    server.sendMessage(spinMessage, robotIPs[playersLeft[0]], udpPort)
                    time.sleep(2)
                    server.sendMessage(stopMessage, robotIPs[playersLeft[0]], udpPort)
                    playersLeft.remove(playersLeft[0])
                for player in playersLeft:
                    if colorDetection.isDetected(player):
                        userInput = controllers.get_data(controllerAddresses[player])
                        commandToSend = getCommand(userInput)
                        server.sendMessage(commandToSend, robotIPs[player], udpPort)
                    else:
                        playersLeft.remove(player)
                        server.sendMessage(stopMessage, robotIPs[player], udpPort)
            elif gamemode == "team":
                if ("Red" in playersLeft or "Yellow" in playersLeft) and ("Blue" not in playersLeft and "Green" not in playersLeft):
                    for player in playersLeft:
                        server.sendMessage(spinMessage, robotIPs[playersLeft[player]], udpPort)
                    time.sleep(2)
                    for player in playersLeft:
                        server.sendMessage(stopMessage, robotIPs[playersLeft[player]], udpPort)
                    gameState = "setup"   
                if ("Blue" in playersLeft or "Green" in playersLeft) and ("Red" not in playersLeft and "Yellow" not in playersLeft):
                    for player in playersLeft:
                        server.sendMessage(spinMessage, robotIPs[playersLeft[player]], udpPort)
                    time.sleep(2)
                    for player in playersLeft:
                        server.sendMessage(stopMessage, robotIPs[playersLeft[player]], udpPort)
                    gameState = "setup"   
                for player in playersLeft:
                    if colorDetection.isDetected(player):
                        userInput = controllers.get_data(controllerAddresses[player])
                        commandToSend = getCommand(userInput)
                        server.sendMessage(commandToSend, robotIPs[player], udpPort)
                    else:
                        playersLeft.remove(player)
                        server.sendMessage(stopMessage, robotIPs[player], udpPort)    


if __name__ == '__main__':
    Main()
 
