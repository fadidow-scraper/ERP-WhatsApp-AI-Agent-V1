import requests
from config import ULTRAMSG_INSTANCE_ID, ULTRAMSG_TOKEN

class WhatsAppAPI:
    def __init__(self):
        self.instance_id = ULTRAMSG_INSTANCE_ID
        self.token = ULTRAMSG_TOKEN
        self.base_url = f"https://ultramsg.com{self.instance_id}/messages/chat"

    def send_message(self, to_number, text):
        payload = {
            "token": self.token,
            "to": to_number,
            "body": text
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.base_url, data=payload, headers=headers)
        return response.json()
