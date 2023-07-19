#!/usr/bin/env python3
'''Inserts a new document in a collection based on kwargs '''


def insert_school(mongo_collection, **kwargs):
    ''' Returns new _id of newly inserted document'''
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
