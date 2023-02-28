from os import getenv
from flask import Flask, render_template,request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask('MFC_MIIT', static_folder=getenv('static_folder'), template_folder=getenv('form_folder'))
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
CORS(app)

soketio = SocketIO(app)


@app.get('/')
@cross_origin()
def form_send():
    return render_template('form.html')


from .auth import login_router
app.register_blueprint(login_router)

from .form import form_router
app.register_blueprint(form_router)

from .config_handler import config_router
app.register_blueprint(config_router)

from .upload_handler import upload_router
app.register_blueprint(upload_router)

from .certificates import status_router
app.register_blueprint(status_router)