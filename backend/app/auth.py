from json import dumps
from flask import Blueprint, request
from flask_cors import cross_origin
from .modules.database import create_connect
from .modules.check_data import check_response
from .modules.access_handler import access_handler

login_router = Blueprint('auth', __name__, url_prefix='/auth')


@login_router.post('/login')
@cross_origin()
def get_login():
    if request.json is None:
        return dumps({'message': 'Ошибка, перезагрузите страницу!', 'resultCode': 2}, ensure_ascii=False), 200

    data = {key: value for key, value in request.json.items()}
    cheker = check_response(data)

    if not cheker:
        return dumps({'message': "Ошибка в данных", 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()

    sql.execute(
        "INSERT INTO users (id, username, first_name, last_name, photo_code) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
        (data['id'], data['username'], data['first_name'], data.get('last_name', ''), data['photo_url']))

    sql.execute("INSERT INTO sessions (token, user_id) VALUES (%s, %s)", (data['hash'], data['id']))

    db.commit()
    db.close()

    return dumps(data, ensure_ascii=False), 200


@login_router.get('/me', endpoint='get_me')
@access_handler()
def get_me(user):
    return dumps(user, ensure_ascii=False), 200


@login_router.get('/logout')
@access_handler()
def do_logout(user):
    db, sql = create_connect()

    sql.execute('UPDATE sessions SET is_active=False WHERE token=%s', (request.headers.get('Authorization', ''),))
    db.commit()

    db.close()
    return dumps({'message': 'Logout success', 'resultCode': 0}), 200
