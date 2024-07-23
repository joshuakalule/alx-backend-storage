#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
Also adds the top most present IPs
"""

import pymongo


def count_methods(collection, method_strs):
    """Helper to count by method."""
    methods = dict()
    for method in method_strs:
        methods[method] = collection.count_documents({'method': method})
    return methods


if __name__ == '__main__':
    nginx = pymongo.MongoClient().logs.nginx
    method_strs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    log_count = nginx.count_documents({})
    print(f"{log_count} logs")

    print("Methods:")
    for k, v in count_methods(nginx, method_strs).items():
        print(f"\tmethod {k}: {v}")

    status = nginx.count_documents({'path': '/status'})
    print(f"{status} status check")

    # Advanced
    print("IPs:")

    pipeline = [
        {'$group': {'_id': "$ip", 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]

    for ip in nginx.aggregate(pipeline):
        print(f"\t{ip['_id']}: {ip['count']}")

