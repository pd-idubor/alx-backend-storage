#!/usr/bin/env python3
"""Describes a Cache class"""
import redis
import uuid
from typing import Optional, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that count how many times methods \
            of the Cache class are called
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper func"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and \
            outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper func"""
        key = method.__qualname__
        input_key = key + ":inputs"
        output_key = key + ":outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


class Cache():
    """Cache class"""
    def __init__(self):
        """Cache init"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[int, str, bytes, float]) -> str:
        """Takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float]:
        """Convert Redis data back to requires format"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, int, float]:
        """Convert data to str"""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        """Convert data to int"""
        return self.get(key, int)


def replay(method: Callable):
    """Display the history of calls of a particular function"""
    r = redis.Redis()
    key = method.__qualname__
    count = r.get(key).decode('utf-8')
    inputs = r.lrange(key + ":inputs", 0, -1)
    outputs = r.lrange(key + ":outputs", 0, -1)
    print("{} was called {} times:".format(key, count))
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, i.decode('utf-8'),
                                     o.decode('utf-8')))
