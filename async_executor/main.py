""" main.py is an entry point for flask and celery"""

from .resources import *

from flask import Flask as FlaskApp
from flask_restful import Api as FlaskApi

flask_app = FlaskApp(__name__)
flask_app.config['SECRET_KEY'] = 'cb79ec51-aba0-40ae-b439-61e5542868dd'

flask_api = FlaskApi(flask_app)

# routing definitions

flask_api.add_resource(TaskGetApi, '/task/<name>')
flask_api.add_resource(TaskPostApi, '/task')
flask_api.add_resource(TasksGetApi, '/tasks')
flask_api.add_resource(UserLoginApi, '/login')
flask_api.add_resource(UserLogoutApi, '/logout')
flask_api.add_resource(UserRegisterApi, '/register')
