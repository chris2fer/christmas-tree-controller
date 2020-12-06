import os
import json
import datetime

import requests
from sms import SMSClient

termid = ""

CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_SECRET = os.getenv("CLOUD_SECRET")
DEVICE_ID = os.getenv("DEVICE_ID")
HELP_MSG = "Did you know you can send me these commands?\n\n \
    Status - I'll tell you if I'm on or off.\n\n \
    On@10pm - Schedule when I automatically turn on."

    
class TempTwilioClient(object):
    
    def send(self, msg):
        pass


def handler(event, context):
    
    req = event.get('queryStringParameters','')

    print(json.dumps(req, indent=2))
    
    twilio = SMSClient()
    token = get_token()
    
    if not token:
        print('No Token Available')
        return {"statusCode": 500,"body": "No Token"} 
    
    body = req.get('Body')
    if 'status' in body.lower():
        print("Status found in body")
        if is_on(token):
            twilio.send(to=req.get('From'), msg="Ho Ho Ho. I am currently shining bright! MERRY CHRISTMAS!!!")
        else:
            twilio.send(to=req.get('From'), msg="Shhhhh. I am currenly off and taking a nap. zZzzZZz")
    elif '@' in body:
        print("Body looks like a schedule request")
        if len(body.split('@')) == 2:
            opp,t = body.split('@')
            print(f'Turning the tree {opp} at {t}')
    else:
        print("No explicit intent found.  Calling Toggle.")
        twilio.send(to=req.get('From'), msg=HELP_MSG)
        toggle_plug(token)

    return {
        "statusCode": 200,
        "body": "ok"
    }
    
    
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


def get_devices(token):

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
        "token": token 
    }
    resp = requests.post(url=url, data=json.dumps(data), params=params, headers=header)


def get_plug_sysinfo(token):
    header = {"Content-Type": "application/json"}
    url = f'https://wap.tplinkcloud.com/?token={token}'
    data = {
        "method":"passthrough", 
        "params": {
            "deviceId": DEVICE_ID, 
            "requestData": json.dumps({"system":{"get_sysinfo":{}}})
        }
    }
    resp = requests.post(url=url, data=json.dumps(data), headers=header)
    return resp.json() #.get('system').get('get_sysinfo')
    
    
def is_on(token: str) -> bool:
    inf = get_plug_sysinfo(token)
    data = json.loads(inf.get('result').get('responseData'))
    print(data)
    state = data['system']['get_sysinfo']['relay_state']
    if state:
        return True
    else:
        return False
        
def is_off(token: str) -> bool:
    if is_on(token):
        return False
    else:
        return True
        
        
def toggle_plug(token):
    inf = get_plug_sysinfo(token)
    data = json.loads(inf.get('result').get('responseData'))
    print(data)
    state = data['system']['get_sysinfo']['relay_state']
    if state:
        toggle_state = 0
    else:
        toggle_state = 1

    req = {
        "method":"passthrough", 
        "params": {
            "deviceId": DEVICE_ID, 
            "requestData": json.dumps({
                "system": {
                    "set_relay_state": {"state":toggle_state}
                }
            } )
        }
    }

    header = {"Content-Type": "application/json"}
    url = 'https://wap.tplinkcloud.com/?token={0}'.format(token)

    resp = requests.post(url=url, data=json.dumps(req), headers=header)
    print(resp.text)


def process_request(req):
    
    if 'status' in ''.lower():
        pass
    
    if ':' in req.get('Body'):
        op,when = req.get('Body').split(':')
