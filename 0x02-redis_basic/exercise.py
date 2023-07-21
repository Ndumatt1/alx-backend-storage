#!/usr/bin/env python3
''' Creates a class Cache '''

import random
import redis
from typing import Union
import uuid


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
        '''str_rand = str(random_uuid)'''
        self._redis.set(random_uuid, data)
        return random_uuid
