#!/usr/bin/env python3
"""Module tracks how many times a particular URL was accessed"""
import redis
import requests
from typing import Callable
from functools import wraps


def count(method: Callable):
    """Tracks how many times a URL is accessed"""
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        """Wrapper func"""
        r.incr(f"count:{url}")
        exp_count = r.get(f"cached:{url}")
        if exp_count:
            return exp_count.decode("utf-8")
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count
def get_page(url: str) -> str:
    """Retrieves HTML content"""
    return requests.get(url).text
