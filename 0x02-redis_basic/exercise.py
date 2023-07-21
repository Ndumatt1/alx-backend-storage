#!/usr/bin/env python3
''' Creates a class Cache '''

import random
import redis
from typing import Union, Optional, Callable
from functools import wraps
import uuid
import json


def count_calls(method: Callable) -> Callable:
    ''' Counts how many times methods of Cache class was called'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrap param self, args, return'''
        self._redis.incr(key)
        return method(self, *args, *kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' Store the history of inputes and outputs for a particular function'''
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper function '''
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    ''' Defines a cache class '''

    def __init__(self):
        ''' Defines an instance of Redis client'''
        self._redis = redis.Redis(decode_responses=True)
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' Generate random key store the input in Redis '''
        rnd = random.Random()
        rnd.seed(123)
        random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))
        self._redis.set(random_uuid, data)
        return random_uuid

    def get(self, key: str, fn: Optional[Callable] = None):
        ''' Takes a key string argument and optional Callble '''
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_str(self, key):
        ''' Converts a redis value to a string '''
        return self.decode('utf-8')

    def get_int(self, key):
        ''' Converts a redis value to an int '''
        return int.from_bytes(self, sys.byteorder)
