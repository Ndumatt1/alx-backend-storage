#!/usr/bin/env python3
''' Provides stats about Nginx logs stored in MongoDB'''


from pymongo import MongoClient


def log_stats():
    ''' Provides some stats about Nginx logs stored in MongoDB'''
    client = MongoClient()

    collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    counts = []
    total_logs = collection.count_documents({})
    status = collection.count_documents({'method': 'GET', 'path': '/status'})

    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    top_ips_list = list(top_ips)

    for method in methods:
        counts.append(collection.count_documents({'method': method}))

    print('{} logs'.format(total_logs))
    print('Methods:')

    for method, count in zip(methods, counts):
        print('\tmethod {}: {}'.format(method, count))
    print('{} status check'.format(status))
    print('IPs:')

    for ips in top_ips_list:
        print('\t{}: {}'.format(ips['_id'], ips['count']))


if __name__ == '__main__':
    log_stats()
