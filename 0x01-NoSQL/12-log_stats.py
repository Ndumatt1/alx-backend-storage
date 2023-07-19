#!/usr/bin/env python3
''' Provides stats about Nginx logs stored in MongoDB'''


from pymongo import MongoClient
import pprint

client = MongoClient()

collection = client.logs.nginx
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
counts = []
total_logs = collection.count_documents({})
get_logs = collection.count_documents({'method': 'GET', 'path': '/status'})

for method in methods:
    counts.append(collection.count_documents({'method': method}))

print('{} logs'.format(total_logs))
print('Methods:')

for method, count in zip(methods, counts):
    print('\tmethod {}: {}'.format(method, count))
print('{} status check'.format(get_logs))
