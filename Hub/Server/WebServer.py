from flask import Flask, render_template, jsonify, g
import threading
import socket

app = Flask(__name__)
state = ""
lock = threading.Lock()
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind(('localhost', 5005))

def getState():
    getStateBytes = b'{"sender": "web", "message": "get state"}'
    serverSock.send(getStateBytes)
    data, addr = serverSock.recvfrom(1024)
    if data:
        return data
    else:
        return "Get State failed"

def setState(toSet):
    getStateBytes = b'{"sender": "web", "message": "set state", "state": "' + toSet + '"}'
    serverSock.send(getStateBytes)

def run():
    app.run()

def runAsync():
    thread = threading.Thread(target = run)
    thread.start()

@app.route('/')
def index():
    newState = "Initialization"
    setState(newState)
    return render_template('index.html', message=newState)

@app.route('/led_on/', methods=['POST'])
def led():
    newState = "LED on"
    setState(newState)
    return render_template('index.html', message=newState)

@app.route('/state/', methods=['GET'])
def handleGetState():
    currState = getState()
    return currState
