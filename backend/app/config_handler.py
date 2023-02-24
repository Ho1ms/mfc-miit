from json import dumps
from flask import Blueprint, request
from .modules.database import create_connect
from .modules.access_handler import access_handler

config_router = Blueprint('config', __name__, url_prefix='/config')


@config_router.get('/messages', endpoint='get_messages')
@access_handler((1,2,3))
def get_messages(user):

    lang_id = request.args.get('lang')

    if not lang_id.isdigit():
        return dumps({'message':'Hacking attempt', 'resultCode':2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute("SELECT type, l.id, title, text, attachment FROM messages "
                "INNER JOIN localisation l on messages.id = l.message_id AND language_id = %s", (lang_id))
    rows = sql.fetchall()
    db.close()
    return dumps(rows, ensure_ascii=False), 200


@config_router.get('/localisations',endpoint='get_localisations')
@access_handler((1,2,3))
def get_localisations(user):
    db, sql = create_connect()

    sql.execute("SELECT * FROM languages ORDER BY id")
    languages = sql.fetchall()

    db.close()
    return dumps(languages, ensure_ascii=False), 200