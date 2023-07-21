#!/usr/bin/env python3
''' Creates a class Cache '''

import random
import redis
from typing import Union, Optional, Callable
import uuid
import json


class Cache:
    ''' Defines a cache class '''

    def __init__(self):
        ''' Defines an instance of Redis client'''
        self._redis = redis.Redis(decode_responses=True)
        self._redis.flushdb()

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
