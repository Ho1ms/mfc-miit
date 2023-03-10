import json
from flask import request as r
from flask_cors import cross_origin
from .database import create_connect


def access_handler(roles: tuple = ()):
    def handle(func):
        @cross_origin()
        def inner(**kwargs):
            auth_token = r.headers.get('Authorization', '')
        
            if len(auth_token) != 64:
                return {'message': 'Undefined token', 'resultCode': 2}, 200

            db, sql = create_connect()

            if len(roles) > 0:
                role_access = f" AND role_id IN %s"
                params = (auth_token, roles)
            else:
                role_access = ""
                params = (auth_token,)

            sql.execute(
                f"""SELECT u.id, first_name, last_name, username, role_id, r.name role, photo_code
                            FROM users u LEFT JOIN roles r on r.id = u.role_id 
                            LEFT JOIN sessions s on u.id = s.user_id AND s.is_active = true
                            WHERE token=%s {role_access}""",
                params
            )
            user = sql.fetchone()
            db.close()

            if user is not None:
                return func(user=user, **kwargs)

            return json.dumps({'message': 'Нет доступа!', 'resultCode': 2}, ensure_ascii=False), 200

        return inner

    return handle
