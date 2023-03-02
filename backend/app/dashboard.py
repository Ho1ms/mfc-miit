import re
import datetime
from json import dumps
from .modules.form_config import *
from flask import Blueprint, request
from .modules.database import create_connect
from .modules.access_handler import access_handler


dashboard_router = Blueprint('form', __name__, url_prefix='/dashboard')

@dashboard_router.get('/')
@access_handler((1,2,3))
def dashboard(user):
    return {},200
