from wiiScale import *

address1 = "00:22:4C:69:01:27"

controller = WiiController()

controller.start(address1)

while True:
    print controller.get_data(address1)
