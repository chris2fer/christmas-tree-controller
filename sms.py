import os
from twilio.rest import Client


ACCOUNT_SID = os.getenv('TWILIO_ACT_SID')
AUTH_TOKEN  = os.getenv('TWILIO_AUTH_TOKEN')
SMS_FROM_NUMBER = os.getenv('TWILIO_SMS_NUMBER')


class SMSClient(object):

    def __init__(self) -> None:
        super().__init__()
        self._client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    def send(self, to, msg):
        message = self._client.messages.create(
            to=to, 
            from_=SMS_FROM_NUMBER,
            body=msg
        )
