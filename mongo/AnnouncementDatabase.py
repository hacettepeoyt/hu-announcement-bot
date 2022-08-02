from pymongo import MongoClient, ReturnDocument
import dns
import config


def fetch_collection():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['hu-announcement-db']
    collection = test_db['announcements-test']

    return collection


def insert_documents(documents):
    collection = fetch_collection()
    collection.insert_many(documents)

    print('New document(s) have been inserted!')


def find(departmentName):
    collection = fetch_collection()
    department = collection.find_one({'department': departmentName})

    return department['announcements']


def find_all():
    collection = fetch_collection()
    documents_all = collection.find()

    return documents_all


def update(department, announcements):
    collection = fetch_collection()
    collection.find_one_and_update({'department': department},
                                   {'$set': {'announcements': announcements}},
                                   return_document=ReturnDocument.AFTER)

    print(f"Announcements updated for {department} department in database!")