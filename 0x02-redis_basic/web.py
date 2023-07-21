#!/usr/bin/env python3
""" Cache module. """
import redis
import requests
from typing import Callable
from functools import wraps


def count_requests(method: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed in the key
    "count:{url}" and return the page HTML content.
    """

    @wraps(method)
    def wrapper(*args, **kwargs):
        """ Wrapper function. """
        url = args[0]
        key = "count:" + url
        r = redis.Redis()
        r.incr(key)
        page = r.get(url)
        if page:
            return page.decode('utf-8')

        page = method(*args, **kwargs)
        r.setex(url, 10, page)
        return page

    return wrapper


def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL and return it.
    """
    r = requests.get(url)
    html = r.text

    return html
