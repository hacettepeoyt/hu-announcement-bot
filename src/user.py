'''
        As well as Announcement module, User module is also another layer
        between Database and other things in the project.

        I write about this layer and abstraction in mongo/user_db

        User module has lots of functions. They all are self explanatory with the name :)
        If the mongo module would be cleared in the future, as well as User module too.
        They are all connected to each other.
'''



from .mongo import user_db 
from .logging import logger


def enroll(user):
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    language = user.language_code

    user_db.enroll(user_id, first_name, last_name, language, ['hu-3', 'hu-13'])
    logger.info(f"{user_id} has been successfully enrolled the database!")


def add_subscription(user_id, department_id):
    subscriptions = user_db.find_subscriptions(user_id)
    subscriptions.append(department_id)
    user_db.update_subscriptions(user_id, subscriptions)
    logger.info(f"Subscriptions has been updated successfully for {user_id}!")

    return subscriptions


def remove_subscription(user_id, department_id):
    subscriptions = user_db.find_subscriptions(user_id)
    subscriptions.remove(department_id)
    user_db.update_subscriptions(user_id, subscriptions)
    logger.info(f"Subscriptions has been updated successfully for {user_id}!")

    return subscriptions


def get_subscriptions(user_id):
    return user_db.find_subscriptions(user_id)


def reset_subscriptions(user_id):
    user_db.update_subscriptions(user_id, [])
    logger.info(f"Subscriptions has been updated successfully for {user_id}!")
    return []


def get_subscribers(department_id):
    return user_db.find_subscribers(department_id)


def set_dnd(user_id, value):
    user_db.set_customs(user_id, 'dnd', value)
    logger.info(f"Notification status has been changed for {user_id} - {value}")


def set_holiday_mode(user_id, value):
    user_db.set_customs(user_id, 'holiday_mode', value)
    logger.info(f"Holiday mode has been changed for {user_id} - {value}")


def set_language(user_id, value):
    user_db.set_customs(user_id, 'language', value)
    logger.info(f"Language has been changed for {user_id} - {value}")


def get_dnd(user_id):
    return user_db.get_property(user_id, 'dnd')


def get_holiday_mode(user_id):
    return user_db.get_property(user_id, 'holiday_mode')


def get_language(user_id):
    return user_db.get_property(user_id, 'language')


def get_properties(user_id, fields):
    return user_db.get_properties(user_id, fields)


def get_customs(user_id):
    fields = ['dnd', 'holiday_mode', 'language']
    customs = user_db.get_properties(user_id, fields)

    return customs['dnd'], customs['holiday_mode'], customs['language']


def get_all_users():
    return user_db.find_all_users()
    
