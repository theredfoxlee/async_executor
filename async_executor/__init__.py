"""
    async_executor is async task scheduler driven by REST Api

    __init__.py initializes FlaskApp, FlaskApi, RabbitmqBroker, and Redis
"""

from dramatiq.brokers.rabbitmq import RabbitmqBroker
from redis import Redis

import dramatiq
import rom

rabbitmq_app = RabbitmqBroker(host="broker", port=5672)
redis_app = Redis(host='backend', port=6379)

redis_app.ping()

rom.util.CONNECTION = redis_app
dramatiq.set_broker(rabbitmq_app)
