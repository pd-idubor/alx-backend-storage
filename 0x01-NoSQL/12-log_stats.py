#!/usr/bin/env python3
"""Defines a func that provides stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


if __name__ == "__main__":
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    doc_num = logs_collection.count_documents({})
    print("{} logs".format(doc_num))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_num = logs_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_num))
    filter_path = {"method": "GET", "path": "/status"}
    num_path = logs_collection.count_documents(filter_path)
    print("{} status check".format(num_path))
