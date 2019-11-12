from Server.UDPserver import *
from Server.Robot import *
from OpenCV.colorDetectionPiCamera import *
from wiiScale import *
import socket
import time

# udp server config
localIP = "127.0.0.1"
udpPort = 5050

# color ranges config
colorRanges = {
    'Red': [([0, 70, 50], [10, 255, 255]), ([170, 70, 50], [180, 255, 255])],
    'Green': [([40, 40, 40], [70, 255, 255])],
    'Blue': [([111, 140, 40], [126, 255, 255])],
    'Yellow': [([20, 40, 40], [35, 255, 255])]
}

colorDetection = ColorDetection(colorRanges, _threshold=5000)

controllerAddresses = {
    'Red': "00:22:4C:69:01:27",
    'Green': "00:24:1E:FC:18:65",
    'Blue': "00:1F:C5:A8:81:55",
    'Yellow': "00:1F:C5:A7:DF:6C"
}

controllers = WiiController()

robotIPs = {
    'Red': "192.168.4.1",
    'Green': "192.168.4.2",
    'Blue': "192.168.4.3",
    'Yellow': "192.168.4.4"
}

robotCommands = RobotCommand()

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, "ACK")

server = udpServer(udpPort, localIP, messageHandler)

def Main():
    # fire up the wii boards
    for key in controllerAddresses:
        controllers.start(controllerAddresses[key])

    colorDetection.startDetection()
    # main game loop
    while True:


if __name__ == '__main__':
    Main()
