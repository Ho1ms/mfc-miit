from json import dumps
from flask import Blueprint, request
from .modules.database import create_connect
from .modules.access_handler import access_handler


config_router = Blueprint('config', __name__, url_prefix='/config')


@config_router.put('/', endpoint='edit_messages')
@access_handler((1,))
def edit_messages(user):
    r = request.json
    type_ = r.get('type')

    if type_ not in ('faq', 'localisation'):
        return dumps({'message': 'Hacking attempt', 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute(f"UPDATE {type_} SET title=%s, text=%s, attachment=%s WHERE id=%s",
                (r.get('title'),
                 r.get('text'),
                 r.get('attachment') if not r.get('img_del') else None, r['id']))
    db.commit()
    db.close()

    return r,200

@config_router.get('/messages', endpoint='get_messages')
@access_handler((1,))
def get_messages(user):
    lang_id = request.args.get('lang')

    if not lang_id.isdigit():
        return dumps({'message': 'Hacking attempt', 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute("SELECT name, l.id, title, text, attachment FROM messages "
                "INNER JOIN localisation l on messages.id = l.message_id AND language_id = %s ORDER BY id", (lang_id,))
    rows = sql.fetchall()
    db.close()
    return dumps(rows, ensure_ascii=False), 200


@config_router.get('/faq', endpoint='get_faq')
@access_handler((1,2))
def get_faq(user):
    lang_id = request.args.get('lang')

    if not lang_id.isdigit():
        return dumps({'message': 'Hacking attempt', 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute("SELECT id, title, text, attachment FROM faq f WHERE language=%s ORDER BY id DESC ", (lang_id,))
    rows = sql.fetchall()
    db.close()
    return dumps(rows, ensure_ascii=False), 200

@config_router.delete('/faq/<int:id>', endpoint='del_faq')
@access_handler((1,2))
def del_faq(user, id):

    if not isinstance(id, int):
        return dumps({'message': 'Hacking attempt', 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute("DELETE FROM faq WHERE id=%s", (id,))
    db.commit()
    db.close()
    return dumps({'message':f'Success deleted #{id}','resultCode':0}, ensure_ascii=False), 200


@config_router.post('/faq', endpoint='add_faq')
@access_handler((1,2))
def add_faq(user):
    data = request.json

    if 'text' not in data or 'title' not in data or 'attachment' not in data or 'lang' not in data:
        return dumps({'message': 'Hacking attempt', 'resultCode': 2}, ensure_ascii=False), 200

    db, sql = create_connect()
    sql.execute("INSERT INTO faq (language, title, text, attachment) VALUES (%s,%s,%s,%s) RETURNING id", (data['lang'], data['title'], data['text'],data['attachment']))
    id = sql.fetchone()['id']
    db.commit()
    db.close()
    return dumps({**data, 'id':id}, ensure_ascii=False), 200


@config_router.get('/localisations', endpoint='get_localisations')
@access_handler((1, 2, 3))
def get_localisations(user):
    db, sql = create_connect()

    sql.execute("SELECT * FROM languages ORDER BY id")
    languages = sql.fetchall()

    db.close()
    return dumps(languages, ensure_ascii=False), 200


@config_router.get('/users', endpoint='get_users')
@access_handler((1, 2, 3))
def get_users(user):
    db, sql = create_connect()
    query = '%' + request.args.get('q','') + '%'
    print(query)
    q_string = ''
    q_arr = ()

    if query:
        q_string = "WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s"
        q_arr = (query,query,query)
    print(q_string)
    sql.execute(f"""SELECT u.id, username, first_name, last_name, photo_code, role_id, r.name role FROM users u LEFT JOIN roles r on r.id = u.role_id 
    {q_string}
    ORDER BY u.id, u.role_id
    """, q_arr)

    users = sql.fetchall()
    print(users)
    db.close()
    return dumps(users, ensure_ascii=False), 200


@config_router.put('/users', endpoint='edit_users')
@access_handler((1,))
def edit_users(user):
    db, sql = create_connect()
    data = request.json
    sql.execute("UPDATE users SET last_name=%s, first_name=%s, role_id=%s WHERE id=%s",
                (data.get('last_name', ''), data.get('first_name', ''), data.get('role_id', '1'), data.get('id')))
    db.commit()

    db.close()
    return dumps({'message': 'Данные изменены!', 'resultCode': 0}, ensure_ascii=False), 200


@config_router.get('/roles', endpoint='get_roles')
@access_handler((1, 2, 3))
def get_roles(user):
    db, sql = create_connect()

    sql.execute("SELECT * FROM roles ORDER BY id")
    roles = sql.fetchall()

    db.close()
    return dumps(roles, ensure_ascii=False), 200
