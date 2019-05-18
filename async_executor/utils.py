import hashlib

from functools import wraps
from flask import session
from flask_restful import abort


def md5(x):
    return hashlib.md5(x.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] is None:
            abort(403, message='permission denied')
        return f(*args, **kwargs)
    return decorated_function
