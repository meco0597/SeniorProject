import socket
import threading
import struct

class udpServer():

    # Server constructor, pass in the port and the delegate for
    # recieving messages. Delegate must take in a string for the
    # data being recieved.
    def __init__(self, _port, _IP, _messageRecievedDelegate):
        self.IP = _IP
        self.port = _port
        self.messageRecievedDelegate = _messageRecievedDelegate
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendBuffer = {}
        self.lock = threading.Lock()
        self.sock.bind(('', self.port))
        print("Server started on host: " + str(self.IP) + " Port: " + str(self.port))


    # helper to get the send buffer since we need to keep it thread safe
    def getSendBuffer(self):
        self.lock.acquire()
        to_return = self.sendBuffer
        self.lock.release()
        return to_return


    # helper to set something in the send buffer to keep it thread safe
    def setSendBuffer(self, key, value):
        self.lock.acquire()
        self.sendBuffer[key] = value
        self.lock.release()


    # The message loop. Will check if there is any incoming messages from any
    # of the clients and call the handler
    def messageLoop(self):
        while True:
            sendBuff = self.getSendBuffer()
            # grab the data recieved from the socket
            data, addr = self.sock.recvfrom(1024)
            # call the handler for new data recieved
            if data:
                self.messageRecievedDelegate(data, addr)
            for address in sendBuff:
                # if there is information to send back then send it
                if sendBuff[address] != "":
                    self.sock.sendto(bytes(sendBuff[address]), addr)


    # This will broadcast data to a multicast ip
    def broadcast(self, data, multicastIP, port):
        multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
        multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        multicast_sock.sendto(data, (multicastIP, port))


    # Sends a basic message
    def sendMessage(self, data, IP, port):
        self.sock.sendto(data, (IP, port))


    # Start the message loop thread that will wait for a messages and send back
    # responses if needed
    def startMessageLoop(self):
        thread = threading.Thread(target = self.messageLoop)
        thread.start()
