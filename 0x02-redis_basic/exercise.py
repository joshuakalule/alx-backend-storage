#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
from typing import Any, Callable, Union
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

    def get(self, key: str, fn: Union[Callable, None] = None) -> Any:
        """Executes redis.get()"""
        if self._redis.exists(key) == 0:
            return None
        data = self._redis.get(key)
        if fn:
            try:
                return fn(data)
            except Exception as e:
                raise e
        return data

    def get_str(self, key: str) -> str:
        """Convert to str"""
        return self.get(key, fn=lambda s: s.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Convert to int"""
        return self.get(key, fn=int)
