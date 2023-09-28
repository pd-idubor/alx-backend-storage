#!/usr/bin/env python3
"""New version- provides some stats about Nginx logs"""
from pymongo import MongoClient


if __name__ == "__main__":
    """
    Sorted log stats
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    row = client.logs.nginx
    print("{} logs".format(row.estimated_document_count()))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = row.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))
    status_get = row.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
    print("IPs:")
    tops = row.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in tops:
        print("\t{}: {}".format(ip.get('ip'), ip.get('count')))
