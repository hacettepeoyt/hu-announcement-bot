from pymongo import MongoClient, ReturnDocument
import dns
import config


def fetch_database():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['hu-announcement-db']
    user_configs = test_db['announcements']

    return user_configs


def find_announcement(departmentName):
    collection = fetch_database()
    department = collection.find_one({'department': departmentName})
    old_announcement = {'title': department['title'], 'content': department['content'], 'url': department['url']}

    return old_announcement


def update_announcements(departmanName, new_announcement):
    collection = fetch_database()
    collection.find_one_and_update({'department': departmanName},
                                   {'$set': {'title': new_announcement['title'], 'content': new_announcement['content'],
                                             'url': new_announcement['url']}},
                                   return_document=ReturnDocument.AFTER)

    print(f"Announcements updated for {departmanName} department in database!")
