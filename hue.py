import json
import requests
import sys
import random
import time

# Returns json object that contains the hue username
def getHueUsername(filename):
    with open(filename) as data:
        d = json.load(data)
    return d["username"]

def getHueBridgeIp(filename):
    with open(filename) as data:
        d = json.load(data)
    return d["ip"]

def getLightsData(username, ip):
    # TODO(Joonas): Check if https is supported
    apiUrl = "http://" + str(ip) + "/api/" + str(username) + "/lights"
    r = requests.get(apiUrl)
    if r.status_code == 200 or r.status_code == 201:
        print("Getting lights Data worked!")
    else:
        print("HTTP GET failed with status code: " + str(r.status_code))
        sys.exit(1)

    return json.loads(r.text)

def getSingleLight(username, ip, lightId):
    apiUrl = "http://" + str(ip) + "/api/" + str(username) + "/lights/" + str(lightId)
    r = requests.get(apiUrl)
    if r.status_code == 200 or r.status_code == 201:
        print("Getting single light Data worked!")
    else:
        print("HTTP GET failed with status code: " + str(r.status_code))
        sys.exit(1)

    print(r.text)
    return json.loads(r.text)

def putLightOn(username, ip, lightId):
    apiUrl = "http://" + str(ip) + "/api/" + str(username) + "/lights/" + str(lightId) + "/state"
    #body = {"on" : False}
    body = {"on": True, "sat":254, "bri":254, "hue": 10000}
    r = requests.put(apiUrl, data=json.dumps(body))
    if r.status_code == 200 or r.status_code == 201:
        print("Putting Light " + str(lightId) + " on worked!")
    else:
        print("HTTP PUT failed with status code: " + str(r.status_code))
        sys.exit(1)

def changeLightColor(username, ip, lightId, color):
    apiUrl = "http://" + str(ip) + "/api/" + str(username) + "/lights/" + str(lightId) + "/state"
    body = {"hue": color}
    r = requests.put(apiUrl, data=json.dumps(body))
    if r.status_code == 200 or r.status_code == 201:
        #print("Putting Light " + str(lightId) + " on worked!")
        pass
    else:
        print("HTTP PUT failed with status code: " + str(r.status_code))
        sys.exit(1)

def main():
    CREDENTIALS_FILE = "credentials.json" # confidental not in GIT
    username = getHueUsername(CREDENTIALS_FILE)
    ip = getHueBridgeIp(CREDENTIALS_FILE)
    lights = getLightsData(username, ip)
    for id in lights:
        putLightOn(username, ip, id)
        light = getSingleLight(username, ip, id)

    while(True):
        for id in lights:
            color = random.randint(0,65535)
            changeLightColor(username, ip, id, color)
        time.sleep(3)

if __name__ == "__main__":
        main()

