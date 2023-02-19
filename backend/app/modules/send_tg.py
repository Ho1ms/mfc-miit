import requests
from os import getenv
def tg_send(message, chat_id):
    requests.post(url=f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage', data={'chat_id': chat_id, 'text': message, 'parse_mode': "HTML"})