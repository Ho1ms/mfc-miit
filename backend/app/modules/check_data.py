import hmac
from os import getenv
from re import fullmatch
from hashlib import sha256


def check_response(data):
    d = data.copy()
    d_list = []

    if not isinstance(d.get('id'),int):
        return False

    elif not fullmatch(r'[a-z0-9]{64}', d.get('hash')):
        return False

    del d['hash']
    for key in sorted(d.keys()):
        if d.get(key, None):
            d_list.append(key + '=' + str(d[key]))

    data_string = bytes('\n'.join(d_list), 'utf-8')

    secret_key = sha256(getenv('BOT_TOKEN').encode('utf-8')).digest()
    hmac_string = hmac.new(secret_key, data_string, sha256).hexdigest()

    return hmac_string == data['hash']
