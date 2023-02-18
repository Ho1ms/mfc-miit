from json import dumps
import os

from flask import Blueprint, request, render_template
from flask_cors import cross_origin
from .modules.database import create_connect
from .modules.check_data import check_response
from .modules.access_handler import access_handler

form_router = Blueprint('form', __name__, url_prefix='/form')


@form_router.get('/')
@cross_origin()
def form_send():
    return render_template('form_1.html')

@form_router.post('/add')
@cross_origin()
def form_add():
    data = request.json
    print(data)
    with open('test.log','w+',encoding='utf-8') as f:
        f.write(str(data))
    return {}, 200