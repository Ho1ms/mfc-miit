import re
import datetime
from json import dumps
from .modules.form_config import *
from flask_cors import cross_origin
from flask import Blueprint, request
from .modules.send_tg import tg_send
from .modules.database import create_connect
from .modules.access_handler import access_handler
from .modules.check_data import check_webapp_signature

form_router = Blueprint('form', __name__, url_prefix='/form')


def check(date):
    try:
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    except TypeError:
        return None
    return d


@form_router.post('/add')
@cross_origin()
def form_add():
    data = request.json

    sign = data.get('sign')
    user = check_webapp_signature(sign)

    if not user:
        return dumps({'message':'Hacking attempt, calling in cyber-police!','resultCode':2}), 403

    type = str(data.get('type'))
    lang = data.get('lang')

    lang = lang if lang in ('en', 'ru') else 'ru'
    type = type if type in ('1', '2') else '1'

    birthday = check(data.get('birthday'))

    if birthday is None or (birthday > datetime.datetime.now() - datetime.timedelta(days=30 * 12 * 5)):
        return dumps({'message': 'Hacking attempt, calling in cyber-police! #1', 'resultCode': 2}), 403

    for param in params[type]:
        if param not in type_settings:
            continue

        if type_settings[param]['type'] == 'text' and not re.fullmatch(type_settings[param]['pattern'],
                                                                       data.get(param, '')):
            return dumps({'message': 'Hacking attempt, calling in cyber-police! #2', 'resultCode': 2}), 403

    if not data['count'].isdigit() or (data['count'].isdigit() and 0 > int(data['count']) > 10):
        return dumps({'message': 'Hacking attempt, calling in cyber-police! #3', 'resultCode': 2}), 403

    if type == '2' and ('date_start' not in data or 'date_end' not in data or not check(data['date_start']) or not check(
            data['date_end'])):
        return dumps({'message': 'Hacking attempt, calling in cyber-police! #3', 'resultCode': 2}), 403

    db, sql = create_connect()

    data['user_id'] = user['id']

    sql.execute(
        f"""INSERT INTO {certs_types[type]} (user_id, {', '.join(params[type])})
         VALUES (%s, {', '.join(['%s' for i in params[type]])})
         RETURNING id""",
        (data.get('user_id'), *[data[i] for i in params[type]])
    )

    form_id = sql.fetchone()['id']
    db.commit()

    sql.execute(
        "SELECT text FROM messages "
        "INNER JOIN localisation l on messages.id = l.message_id "
        "INNER JOIN languages l2 on l2.id = l.language_id"
        " WHERE type = 'backend_form_success' AND code=%s ",
        (lang,)
    )
    msg_footer = sql.fetchone()['text']
    db.close()

    msg = f'<b>{titles[lang][type]}</b> <code>#{form_id}</code>\n\n'

    for key in params[type]:
        msg += f"<b>{config[lang][key]}:</b> <code>{data[key]}</code>\n"

    msg += f'\n{msg_footer}'

    tg_send(msg, user['id'])
    return {'message': 'ok', 'resultCode': 0}, 200


@form_router.get('/get-form')
@cross_origin()
def get_form():
    if request.args is None:
        return {'message': 'Missing args'}, 400

    type = request.args.get('type')
    lang = request.args.get('lang')

    lang = lang if lang in ('en', 'ru') else 'ru'
    type = type if type in ('1', '2') else '1'

    data = {}

    type_settings['birthday']['max'] = (datetime.datetime.now() - datetime.timedelta(days=365 * 5)).strftime('%Y-%m-%d')

    for key in params[type]:
        data[key] = {
            'name': config[lang][key],
            'data': type_settings[key]
        }

    return dumps({'names': params[type], 'title': titles[lang][type], 'data': data, 'button': btn_name[lang]},
                 ensure_ascii=False), 200


@form_router.get('/get-forms', endpoint='get_forms')
@access_handler((1, 2, 3))
def get_forms(user):
    db, sql = create_connect()

    type = request.args.get('type')
    if not type.isdigit():
        return {}, 403

    sql.execute(
        f"SELECT c.id, username, c.last_name, c.name, c.father_name, email, to_char(birthday,'dd.mm.YYYY') birthday, group_name,  to_char(create_at,  'HH24:MM dd.mm.YYYY') create_at, status FROM {certs_types[type]} c INNER JOIN bot_users bu on c.user_id = bu.id")
    rows = sql.fetchall()

    db.close()

    return dumps(rows, ensure_ascii=False), 200


@form_router.get('/cert-list',endpoint='get_certs_list')
@access_handler((1,2,3))
def get_certs_list(user):
    types = [
        {'type':'1','title':'с места учёбы'},
        {'type':'2','title':'о размере стипендии'},
    ]

    return dumps(types, ensure_ascii=False), 200