#!/usr/bin/env python3
''' Returns all students sorted by average score '''


def top_students(mongo_collection):
    ''' Returns all students sorted by average score '''
    pipeline = [
            {
                "$addFields": {
                    "averageScore": {"$avg": "$topics.score"}
                    }
            },
            {
                "$sort": {"averageScore": -1}
            }
            ]
    result = mongo_collection.aggregate(pipeline)
    return list(result)
