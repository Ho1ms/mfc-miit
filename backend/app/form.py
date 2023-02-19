from json import dumps
import os
import datetime
from flask import Blueprint, request, render_template
from flask_cors import cross_origin
from .modules.database import create_connect
from .modules.check_data import check_response
from .modules.access_handler import access_handler
from .modules.send_tg import tg_send
from .modules.form_config import *

form_router = Blueprint('form', __name__, url_prefix='/form')


@form_router.get('/')
@cross_origin()
def form_send():
    return render_template('form.html')


def check(date):
    try:
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    return d


@form_router.post('/add')
@cross_origin()
def form_add():
    data = request.json
    type = data.get('type')
    lang = data.get('lang')
    lang = lang if lang in ('en', 'ru') else 'ru'

    birthday = check(data.get('birthday'))

    if (type not in ('1', '2')) or (not isinstance(data.get('user_id'), int)) or (
            birthday > datetime.datetime.now() - datetime.timedelta(days=30 * 12 * 5)):
        return {}, 400

    if type == '2' and (not check(data.get('date_start')) or not check(data.get('date_end'))):
        return {}, 400

    db, sql = create_connect()

    sql.execute(
        f"INSERT INTO certificates (user_id, type, {', '.join(params[type])}) VALUES (%s, %s, {', '.join(['%s' for i in params[type]])}) RETURNING id",
        (data.get('user_id'), type, *[data[i] for i in params[type] ])
    )

    form_id = sql.fetchone()['id']
    db.commit()
    db.close()

    msg = f'<b>{titles[lang][type]}</b> <code>#{form_id}</code>\n\n'

    for key in params[type]:
        msg += f"<b>{config[lang][key]}:</b> <code>{data[key]}</code>\n"

    if lang == 'ru':
        msg += """\n<b>Ваша заявка принята.</b>
⏳ <b>Срок изготовления справок –</b><code> 3 рабочих дня. </code>

📧 <b>По готовности на указанную Вами почту будет направлено уведомление о готовности. </b>

📕 <b>Оригинал справки о размере стипендии Вы сможете забрать по адресу:</b> <code>ул. Образцова, 9 стр.9, 10 корпус, 3 этаж, каб. 10310.</code>

⏰ <b>Часы работы: </b>
🍽 <b>Обед:</b> <code>с 12.00 до 13.00 </code>
👨‍💻 <b>пн – чт:</b> <code>с 9.00 до 18.00 </code>
👨‍💻 <b>пт:</b> <code>с 9.00 до 17.00 </code>"""
    else:
        msg += """\n<b>Your application has been accepted.</b>
⏳ <b>The deadline for making references is</b><code> 3 working days. </code>

📧 <b>Upon readiness, a notification of readiness will be sent to the e-mail address specified by You. </b>

📕 <b>You can pick up the original certificate of the scholarship amount at the address:</b> <code>Obraztsova str., 9 p.9, 10 building, 3rd floor, office 10310.</code>

⏰ <b>Opening hours: </b>
🍽 <b>Lunch:</b> <code>from 12.00 to 13.00 </code>
👨‍💻 <b>Mon – Thu:</b> <code>from 9.00 to 18.00 </code>
👨‍💻 <b>Fri:</b> <code>from 9.00 to 17.00 </code>"""

    tg_send(msg, data['user_id'])
    return data, 200


@form_router.get('/get-form')
@cross_origin()
def get_form():
    if request.args is None:
        return {'message': 'Missing args'}, 400

    type = request.args.get('type')
    lang = request.args.get('lang')
    lang = lang if lang in ('en', 'ru') else 'ru'

    data = {}

    for key in params[type]:
        data[key] = {
            'name': config[lang][key],
            'data': type_settings[key]
        }

    return dumps({'names': params[type], 'title': titles[lang][type], 'data': data,'button': btn_name[lang]}, ensure_ascii=False), 200


@form_router.get('/get-forms')
@access_handler((1, 2, 3))
def get_forms(user):
    db, sql = create_connect()
    sql.execute("SELECT c.id, username, c.last_name || ' ' || substring(c.name,  0, 2) || '. ' || substring(c.father_name,  0, 2) || '.' author, email, to_char(birthday,'dd.mm.YYYY') birthday, group_name,  to_char(create_at,  'HH24:MM dd.mm.YYYY') create_at FROM certificates c INNER JOIN bot_users bu on c.user_id = bu.id")
    rows = sql.fetchall()
    db.close()
    print(rows)
    return dumps(rows, ensure_ascii=False), 200
