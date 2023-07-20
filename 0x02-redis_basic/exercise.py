#!/usr/bin/env python3
"""Describes a Cache class"""
import redis
import uuid
from typing import Optional, Callable, Union


class Cache():
    """Cache class"""
    def __init__(self):
        """Cache init"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
