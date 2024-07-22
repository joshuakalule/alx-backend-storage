#!/usr/bin/env python3
"""Script that provides some stats about Nginx logs stored in MongoDB"""

import pymongo


def count_methods(collection, method_strs):
    """Helper to count by method."""
    methods = dict()
    for method in method_strs:
        methods[method] = collection.count_documents({'method': method})
    return methods


if __name__ == '__main__':
    collection_nginx = pymongo.MongoClient().logs.nginx
    method_strs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    print("Methods:")
    for k, v in count_methods(collection_nginx, method_strs).items():
        print(f"    method {k}: {v}")

    status = collection_nginx.count_documents({'path': '/status'})
    print(f"{status} status check")
