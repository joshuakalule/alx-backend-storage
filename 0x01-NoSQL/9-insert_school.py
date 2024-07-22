#!/usr/bin/env python3
"""Function that inserts new document in a collection."""


def insert_school(mongo_collection, **kwargs):
    """Inserts new documment in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
