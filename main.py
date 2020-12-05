import os
import json

import requests


CLOUD_USER = os.getenv("CLOUDUSER")
CLOUD_SECRET = os.getenv("CLOUDSECRET")
DEVICE_ID = os.getenv("DEVICEID")

def get_token():
    payload = {
     "method": "login",
     "params": {
     "appType": "Kasa_Android",
     "cloudUserName": CLOUD_USER,
     "cloudPassword": CLOUD_SECRET,
     "terminalUUID": termid
     }
    }

    header = {"Content-Type": "application/json"}
    url = 'https://wap.tplinkcloud.com'
    resp = requests.post(url=url, data=json.dumps(payload), headers=header)

    return resp.json().get('result').get('token')

def get_devices():

    header = {"Content-Type": "application/json"}
    data = { "method": "getDeviceList" }
    url = 'https://wap.tplinkcloud.com'
    params = {
        "appName": "Kasa_Android",
        "termID": termid,
        "appVer": "1.4.4.607",
        "ospf": "Android+6.0.1",
        "netType": "wifi",
        "locale": "es_ES",
        "token": "" #TODO: Hmmm this thing looked like a quid.  Forgot how i got it
    }

    resp = requests.post(url=url, data=json.dumps(data), params=params, headers=header)
    # return resp.json().get('result').get('deviceList')
    for dv in get_devices():
        print(dv)

def toggle_device(token):
    command = {"smartlife.iot.smartbulb.lightingservice": {"transition_light_state": {"on_off": 1}}}
    data = {
        "method": "passthrough",
        "params": {
            "deviceId": DEVICE_ID,
            "requestData": json.dumps(command)
        }
    }

    header = {"Content-Type": "application/json"}
    url = 'https://use1-wap.tplinkcloud.com/?token={0}'.format(token)

    resp = requests.post(url=url, data=json.dumps(data), headers=header)
    print(resp.text)


def get_state():

    header = {"Content-Type": "application/json"}
    command = {}
    data = {}