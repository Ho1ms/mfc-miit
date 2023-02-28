import requests
from os import getenv
def tg_send(message, chat_id, reply_to_message_id=None):
    return requests.post(url=f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage', data={'chat_id': chat_id, 'text': message, 'parse_mode': "HTML",'reply_to_message_id':reply_to_message_id}).json()