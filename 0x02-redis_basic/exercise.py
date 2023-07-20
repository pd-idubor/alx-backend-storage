#!/usr/bin/env python3
"""Describes a Cache class"""
import redis
import uuid
from typing import Union


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
