import struct

def decToBin(num, numBits):
    strToFormat = '{0:0' + str(numBits) + 'b}'
    return strToFormat.format(num)
        

class Robot():

    # opcodes for robot communication
    commandToBin = {"Assign":"00000001",
    "Rotate Right": "00000101",
    "Rotate Left": "00000110",
    "Move Forward": "00000111",
    "Move Backward": "00000100",
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

    def __init__(self, _id):
        self.id = _id

    def robotMessage(self, command, param1, param2):
        toReturn = decToBin(self.id, 4) + self.commandToBin[command] + decToBin(param1, 10) + decToBin(param2, 10)
        print(toReturn)
        return struct.pack('>I', int(toReturn, 2))

