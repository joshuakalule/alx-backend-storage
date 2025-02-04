#!/usr/bin/env python3
"""Lists all documents in a collection."""


def list_all(mongo_collection):
    """List all documents in mongo_collection."""
    return list(mongo_collection.find())
