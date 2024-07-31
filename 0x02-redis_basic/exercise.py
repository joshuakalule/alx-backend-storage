#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
from typing import Union
from uuid import uuid4


class Cache:
    """
    Cache class

    Attributes:
    -----------
    _redis: instance of the Redis client

    Methods:
    -----------
    store(data):
        stores data using a random key
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in redis using a random key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
