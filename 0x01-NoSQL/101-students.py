#!/usr/bin/env python3
"""Function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """Returns students sorted by average score"""
    updates = dict()
    # 1: get average score
    for student in mongo_collection.find():
        total = sum((t['score'] for t in student.get('topics')))
        n = len(student['topics'])
        average = total / n
        updates[student['_id']] = average

    # 2: insert average
    for id, avg in updates.items():
        mongo_collection.update_one(
            {'_id': id},
            {'$set': {'averageScore': avg}}
        )

    # 3: return students sorted
    return mongo_collection.find(sort=[('averageScore', -1), ('_id', -1)])
