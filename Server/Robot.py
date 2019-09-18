def decToBin(num, numBits):
    return format(num, "0" + str(numBits) + "b")

class Robot():

    # member variables
    id = -1

    # opcodes for robot communication
    commandToBin = {"Assign":"00000001",
    "Rotate Right": "00001101",
    "Rotate Left": "00001110",
    "Move Forward": "00001111",
    "Move Backward": "00001100",
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
        id = _id

    def robotMessage(self, command, param1, param2):
        toReturn = decToBin(id, 4) + self.commandToBin[command] + decToBin(param1, 10) + decToBin(param2, 10)
        return bytes(toReturn)


