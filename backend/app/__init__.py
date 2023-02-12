from os import getenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask('MFC_MIIT', static_url_path=getenv('static_folder'))
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
CORS(app)

soketio = SocketIO(app)

from .auth import login_router
app.register_blueprint(login_router)
