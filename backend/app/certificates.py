from json import dumps
from .modules.form_config import *
from flask import Blueprint, request
from .modules.send_tg import tg_send
from .modules.database import create_connect
from .modules.access_handler import access_handler

status_router = Blueprint('status',__name__, url_prefix='/status')


@status_router.post('/next', endpoint='status_handler')
@access_handler((1,2,3))
def status_handler(user):
    cert_id = request.json.get('id')
    certs_type = request.json.get('type')

    if not isinstance(cert_id, int) or str(certs_type) not in certs_types:
        return dumps({'message':'Hacking attempt!', 'resultCode':2}, ensure_ascii=False), 200

    status_queue = ['new', 'active', 'ready', 'closed']
    db, sql = create_connect()
    sql.execute(f"SELECT status, user_id, msg_id FROM {certs_types[certs_type]} WHERE id=%s",(cert_id,))
    row = sql.fetchone()
    status = row['status']

    if status is None or status == 'closed':
        db.close()
        return dumps({'message':'Hacking attempt!', 'resultCode':2}, ensure_ascii=False), 200

    next_status_index = status_queue.index(status)+1
    next_status = status_queue[next_status_index]

    sql.execute(f"UPDATE {certs_types[certs_type]} SET status=%s, worker_{next_status}=%s, date_{next_status}=CURRENT_TIMESTAMP WHERE id=%s", ( next_status, user['id'], cert_id))
    db.commit()

    sql.execute(f"""SELECT text FROM messages
    INNER JOIN localisation l on messages.id = l.message_id
    INNER JOIN languages l2 on l2.id = l.language_id WHERE type='backend_form_{next_status}' AND code = (SELECT lang FROM {certs_types[certs_type]} c WHERE c.id=%s)""",(cert_id, ))
    text = sql.fetchone()['text']

    tg_send(text, row['user_id'], row['msg_id'])

    db.close()
    return dumps({'status':next_status}, ensure_ascii=False), 200