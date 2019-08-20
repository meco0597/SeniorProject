import WebServer
import time
import requests

requestURL = "http://localhost:5000/"

def main():
    WebServer.runAsync()
    time.sleep(5)
    while True:
        req = requests.get(url = requestURL + "state/")
        print("Still going... Current State:" + req.text)
        time.sleep(5)

if __name__ == '__main__':
    main()
