# redis_queue.py
from rq import Queue

from redis_service import RedisService


class RedisQueue:
    high = Queue("high", connection=RedisService.get_instance())
    low = Queue("low", connection=RedisService.get_instance())