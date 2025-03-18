import requests
import time
import json


class TG_bot():
    def __init__(self, mediator):
        with open('conf.json', 'r') as file:
            config = json.load(file)
        self.token = config['tg_bot_token']
        self.chat_id = config['alert_tg_chat_id']
        self.mediator = mediator

        commands = [
            {'command': 'status', 'description': 'Check listener status'},
            {'command': 'scan', 'description': 'Start nmap scanning'},
            {'command': 'settings', 'description': 'Get current hosts to scan'}
        ]
        url = f"https://api.telegram.org/bot{self.token}/setMyCommands"
        data = {
            'commands': [{'command': cmd['command'], 'description': cmd['description']} for cmd in commands],
            'scope': {'type': 'chat', 'chat_id': self.chat_id}
        }
        try:
            response = requests.post(url, json=data)
            print(response.json)
        except Exception as exc:
            print(exc)

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {'chat_id': self.chat_id, 'text': message}
        try:
            response = requests.post(url, params=params)
            return response.json()
        except Exception as exc:
            print(f"Can't send message: {exc}")
            return False

    def delete_message(self, message_id):
        url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
        params = {'chat_id': self.chat_id, 'message_id': message_id}
        try:
            requests.post(url, params=params)
        except Exception as exc:
            print(f"Can't delete message: {exc}")

    def get_updates(self, offset=None):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        params = {'timeout': 100, 'offset': offset}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as exc:
            print(f"Can't get updates: {exc}")
            return {"error": f"Can't get updates: {exc}"}

    def run_bot(self):
        last_update_id = None
        while True:
            updates = self.get_updates(last_update_id)
            if "result" in updates:
                for update in updates["result"]:
                    if 'message' in update and 'text' in update['message']:
                        last_update_id = update["update_id"] + 1
                        message_text = update["message"]["text"]
                        if 'scan' in message_text.lower():
                            self.mediator.handle_request('scan')
                        if 'status' in message_text.lower():
                            self.mediator.handle_request('status')
                        if 'settings' in message_text.lower():
                            self.mediator.handle_request('settings')
            time.sleep(1)
