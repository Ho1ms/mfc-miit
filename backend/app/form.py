import re
import datetime
from json import dumps, loads
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

    lang = lang if lang in titles else 'ru'
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
        f"""INSERT INTO {certs_types[type]} (user_id, lang, {', '.join(params[type])})
         VALUES (%s, %s,{', '.join(['%s' for i in params[type]])})
         RETURNING id""",
        (data.get('user_id'),lang, *[data[i] for i in params[type]])
    )
    form_id = sql.fetchone()['id']


    sql.execute(
        "SELECT text FROM messages "
        "INNER JOIN localisation l on messages.id = l.message_id "
        "INNER JOIN languages l2 on l2.id = l.language_id"
        " WHERE type = 'backend_form_success' AND code=%s ",
        (lang,)
    )
    msg_footer = sql.fetchone()['text']


    msg = f'<b>{titles[lang][type]}</b> <code>#{form_id}</code>\n\n'

    for key in params[type]:
        msg += f"<b>{config[lang][key]}:</b> <code>{data[key]}</code>\n"

    msg += f'\n{msg_footer}'

    msg_id = tg_send(msg, user['id']).get('result',{}).get('message_id')

    sql.execute(f"UPDATE {certs_types[type]} SET msg_id=%s WHERE id=%s",(msg_id,form_id))

    db.commit()
    db.close()
    return {'message': 'ok', 'resultCode': 0}, 200


@form_router.get('/get-form')
@cross_origin()
def get_form():
    if request.args is None:
        return {'message': 'Missing args'}, 400

    type = request.args.get('type')
    lang = request.args.get('lang')

    lang = lang if lang in titles else 'ru'
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

    type_ = request.args.get('type')
    filter_ = request.args.get('filter')

    if not type_.isdigit() or filter_ is None:
        return {}, 403

    filter_ = loads(filter_)
    cert_id = '%' + str(filter_.get('id')) + '%'
    group_name = '%' + str(filter_.get('group_name')) + '%'
    author = '%' + str(filter_.get('author')) + '%'
    statuses = filter_.get('statuses')
    sort_by_new = filter_.get('sort_by_new')
    limit = filter_.get('limit')


    sql.execute(
        f"""SELECT c.id, username, c.last_name, c.name, c.father_name, email, to_char(birthday,'dd.mm.YYYY') birthday,
         group_name,  to_char(create_at,  'HH24:MM dd.mm.YYYY') create_at, status,count {", to_char(date_start,'dd.mm.YYYY') date_start, to_char(date_end,'dd.mm.YYYY') date_end" if type=='2' else ''} 
         FROM {certs_types[type_]} c INNER JOIN bot_users bu on c.user_id = bu.id 
         WHERE c.id::text LIKE %s AND group_name LIKE %s AND c.last_name || ' ' || c.name || ' ' || c.father_name LIKE %s AND
         c.status =ANY(%s) ORDER BY id {'DESC' if sort_by_new else 'ASC'} LIMIT %s""", (cert_id, group_name, author, statuses, limit))

    rows = sql.fetchall()

    db.close()

    return dumps(rows, ensure_ascii=False), 200


@form_router.get('/cert-list',endpoint='get_certs_list')
@access_handler((1,2,3))
def get_certs_list(user):
    types = [
        {'type':'1','title':'?? ?????????? ??????????'},
        {'type':'2','title':'?? ?????????????? ??????????????????'},
    ]

    return dumps(types, ensure_ascii=False), 200


