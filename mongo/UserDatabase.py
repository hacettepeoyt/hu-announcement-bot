from pymongo import MongoClient, ReturnDocument
import dns
import config


def fetch_collection():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['hu-announcement-db']
    collection = test_db['user_configs-test']

    return collection


def find_subscribers(departmentName):
    user_configs = fetch_collection()
    users = user_configs.find({"departments": departmentName})

    subscribedUsers = []
    for user in users:
        subscribedUsers.append(user['user_id'])

    return subscribedUsers


def find_subscriptions(user_id):
    user_configs = fetch_collection()
    user = user_configs.find_one({'user_id': user_id})

    return user['departments']


def find_all_users():
    user_configs = fetch_collection()
    users = user_configs.find()
    user_IDs = []

    for user in users:
        user_IDs.append(user['user_id'])

    return user_IDs


def enroll(user_id, first_name, last_name, lang, def_deps):
    user_configs = fetch_collection()
    user = user_configs.find_one({'user_id': user_id})

    if user is None:
        user_info = {'user_id': user_id, 'first_name': first_name,
                     'last_name': last_name, 'dnd': False,
                     'holiday_mode': False, 'language': lang,
                     'departments': def_deps}

        user_configs.insert_one(user_info)


def update_subscriptions(user_id, subscribedDepartments):
    user_configs = fetch_collection()
    user_configs.find_one_and_update({'user_id': user_id},
                                     {'$set': {'departments': subscribedDepartments}},
                                     return_document=ReturnDocument.AFTER)


def set_customs(user_id, key, value):
    user_configs = fetch_collection()
    user_configs.find_one_and_update({'user_id': user_id},
                                     {'$set': {key: value}})


def get_property(user_id, field):
    user_configs = fetch_collection()
    query = {'user_id': user_id}

    return user_configs.find_one(query, {'_id': 0, field: 1})[field]


def get_properties(user_id, fields):
    user_configs = fetch_collection()
    query = {'user_id': user_id}

    dict = {
        '_id': 0
    }

    for field in fields:
        dict[field] = 1

    return user_configs.find_one(query, dict)