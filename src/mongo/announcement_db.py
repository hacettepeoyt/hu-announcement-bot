'''
        Announcement related data is stored in MongoDB. This module helps us to
        fetch and update those announcements.

        To be more clear, I added a layer between database and Telegram API,
        it makes the code more readable and more editable. You can find the layer
        in src folder.

        AnnouncementDatabase and UserDatabase modules can be optimised, because some
        functions do similar things. However, I'm not the guy who tries to optimise
        everything. So, I leave it that way. Maybe in the future, I get bored and
        clear things up again. If you are reading this and want to contribute, here
        you go. I won't open an issue about this.
'''



from pymongo import MongoClient, ReturnDocument
import dns
import config


def fetch_collection():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['hu-announcement-db']
    collection = test_db['announcements']

    return collection


def insert_documents(documents):
    collection = fetch_collection()
    collection.insert_many(documents)


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
                                   
