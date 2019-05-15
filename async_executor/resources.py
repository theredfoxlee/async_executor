from flask_restful import Resource, reqparse, abort
from .utils import login_required
from .resources import Task, User
from .tasks import remote_exec
from flask import session

import uuid


class TaskGetApi(Resource):

    @login_required
    def get(self, name):
        try:
            j = Task.get_by(name).json()
            if j.reporter != session['username']:
                raise AttributeError
            return j
        except AttributeError as e:
            print(e)
            abort(404, message=f"unknown task: {name}")


class TaskPostApi(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('args', type=str, location='json')

    @login_required
    def post(self):
        json_data = self.parser.parse_args()
        args = json_data['args']
        task_name = str(uuid.uuid4())
        t = Task.create(
            name=task_name,
            args=args,
            reporter=User.get_by(session['username'])
        )
        t.save()
        remote_exec.send(task_name, args)
        return t.json()


class TasksGetApi(Resource):

    @login_required
    def get(self):
        return [i.json() for i in Task.query.filter(
            reporter=User.get_by(session['username']).id).execute()]


class UserRegisterApi(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')

    def post(self):
        json_data = self.parser.parse_args()
        username = json_data['username']
        password = json_data['password']
        u = User.create(username, password)
        u.save()
        return {'status': 'ok'}


class UserLoginApi(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')

    def post(self):
        json_data = self.parser.parse_args()
        username = json_data['username']
        password = json_data['password']
        u = User.get_by(username)
        if u.compare(password):
            session['username'] = u.json()['name']
            return {'status': 'ok'}
        else:
            return {'status': 'not ok'}
        return {'status': 'ok'}


class UserLogoutApi(Resource):

    @login_required
    def get(self):
        session.pop('username')
        return {'status', 'ok'}
