from pynput import keyboard
import socket
import time
from time import sleep
from threading import Thread
 
UDP_IP = "192.168.1.128"
UDP_PORT = 5050
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Client part (port 5050 is used by windows?)
cSock.bind(("", 5051))
cSock.setblocking(0)
notDead = True
pressedKeys = {}
 
print("TARGET IP", UDP_IP)
print("TARGET PORT", UDP_PORT)
print("Use arrow keys to control the robot.")
print("Press 'b' for the battery voltage.")
print("To exit, press escape.")
 
def on_press(key):
   pressedKeys[key] = True
 
def on_release(key):
   if key == keyboard.Key.esc:
       # Stop listener
       return False

   pressedKeys[key] = False
 
def senderPrint(msg):
  sock.sendto(bytearray.fromhex(msg), (UDP_IP, UDP_PORT))

# Spams out UDP packets
def spam():
  while notDead:
    if pressedKeys.get(keyboard.KeyCode.from_char('b')):
      senderPrint("0F03E800")
    elif pressedKeys.get(keyboard.Key.up):
      senderPrint("005FFFFF")
    elif pressedKeys.get(keyboard.Key.left):
      senderPrint("007000FF")
    elif pressedKeys.get(keyboard.Key.down):
      senderPrint("006FFFFF")
    elif pressedKeys.get(keyboard.Key.right):
      senderPrint("004000FF")
    else:
      senderPrint("00400000")

    # Receive stuff
    try:
      data, addr = cSock.recvfrom(1024)
      print("Battery Voltage: " + data.decode("utf-8"))
    except:
      pass

    sleep(0.05)

t1 = Thread(target = spam)
t1.start()
 
# Collect events until released
with keyboard.Listener(
       on_press=on_press,
       on_release=on_release) as listener:
   listener.join()

notDead = False
t1.join()


