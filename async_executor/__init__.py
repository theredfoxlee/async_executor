"""
    async_executor is async task scheduler driven by REST Api

    __init__.py initializes FlaskApp, FlaskApi, RabbitmqBroker, and Redis
"""

from flask import Flask as FlaskApp
from flask_restful import Api as FlaskApi
from rabbitmq import RabbitmqBroker
from redis import Redis

import dramatiq
import rom

flask_app = FlaskApp(__name__)
flask_app.config['SECRET_KEY'] = 'cb79ec51-aba0-40ae-b439-61e5542868dd'

flask_api = FlaskApi(flask_app)

rabbitmq_app = RabbitmqBroker(host="localhost", port=5672)
redis_app = Redis(host='localhost', port=6379)

redis_app.ping()

rom.util.CONNECTION = redis_app
dramatiq.set_broker(rabbitmq_app)
