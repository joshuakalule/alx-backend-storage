#!/usr/bin/env python3
"""Writing strings to Redis"""

import redis
from functools import wraps
from typing import Any, Callable, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls made to method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function."""
        method_key = str(method.__qualname__)
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function."""
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        return_value = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, return_value)
        return return_value
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of method."""
    if not hasattr(method, '__self__'):
        return
    _redis = method.__self__._redis
    method_key = str(method.__qualname__)

    count = _redis.get(method_key)
    inputs = _redis.lrange(method_key+':inputs', 0, -1)
    outputs = _redis.lrange(method_key+':outputs', 0, -1)

    print(f"{method_key} was called {int(count)} times:")
    for input, output in zip(inputs, outputs):
        decoded_input = input.decode("utf-8")
        decoded_output = output.decode("utf-8")
        print(f"{method_key}(*{decoded_input}) -> {decoded_output}")


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

    @call_history
    @count_calls
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
