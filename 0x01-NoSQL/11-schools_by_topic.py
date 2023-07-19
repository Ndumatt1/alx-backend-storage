#!/usr/bin/env python3
''' Returns list of school having a specific topic'''


def schools_by_topic(mongo_collection, topic):
    ''' Returns list of school having a specific topic'''
    result = mongo_collection.find({'topics': topic})
    return list(result)
