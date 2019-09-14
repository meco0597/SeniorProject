from Server.UDPserver import *
import Server.WebServer
import socket
import time

# udp server config
localIP = "192.168.4.1"
udpPort = 5050
message = b"Hello ESP"
controllerToRobot = {}
commandToBin = {"Assign":"00000001",
"Move":"00000100",
"Stop": "00001000",
"Read": "11110000",
"Write": "11100000",
"Accelx": "11110001",
"Accely": "11110010",
"Accelz": "11110011",
"Rotx": "11110100",
"Roty": "11110101",
"Rotz": "11110110",
"Posx": "11110111",
"Posy": "11111000",
"Posz": "11111001",
"Batt": "11111010",
"Temp": "11111011",
}

def messageHandler(data, addr):
    print(data)
    server.setSendBuffer(addr, b"ACK")


server = udpServer(udpPort, localIP, messageHandler)


def robotMessage(ID, command, param1, param2):
    toReturn = ID + commandToBin[command] + param1 + param2
    return bytes(toReturn)



def Main():
    server.startMessageLoop()



if __name__ == '__main__':
    Main()