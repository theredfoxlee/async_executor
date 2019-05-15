""" main.py is an entry point for flask and celery"""

from .resources import *
from . import flask_api

# routing definitions

flask_api.add_resource(TaskGetApi, '/task/<name>')
flask_api.add_resource(TaskPostApi, '/task')
flask_api.add_resource(TasksGetApi, '/tasks')
flask_api.add_resource(UserLoginApi, '/login')
flask_api.add_resource(UserLogoutApi, '/logout')
flask_api.add_resource(UserRegisterApi, '/register')
