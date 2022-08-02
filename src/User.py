from mongo import UserDatabase


def enroll(user):
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    language = user.language_code

    UserDatabase.enroll(user_id, first_name, last_name, language, ['hu-3', 'hu-13'])


def add_subscription(user_id, department_id):
    subscriptions = UserDatabase.find_subscriptions(user_id)
    subscriptions.append(department_id)
    UserDatabase.update_subscriptions(user_id, subscriptions)
    return subscriptions


def remove_subscription(user_id, department_id):
    subscriptions = UserDatabase.find_subscriptions(user_id)
    subscriptions.remove(department_id)
    UserDatabase.update_subscriptions(user_id, subscriptions)
    return subscriptions


def get_subscriptions(user_id):
    return UserDatabase.find_subscriptions(user_id)


def reset_subscriptions(user_id):
    UserDatabase.update_subscriptions(user_id, [])
    return []


def set_notification(user_id, value):
    UserDatabase.set_customs(user_id, 'notification_status', value)
    print(f"Notification status has been changed for {user_id} - {value}")


def set_holiday_mode(user_id, value):
    UserDatabase.set_customs(user_id, 'holiday_mode', value)
    print(f"Holiday mode has been changed for {user_id} - {value}")


def set_language(user_id, value):
    UserDatabase.set_customs(user_id, 'language', value)
    print(f"Language has been changed for {user_id} - {value}")


def get_dnd(user_id):
    return UserDatabase.get_property(user_id, 'dnd')


def get_holiday_mode(user_id):
    return UserDatabase.get_property(user_id, 'holiday_mode')


def get_language(user_id):
    return UserDatabase.get_property(user_id, 'language')


def get_properties(user_id, fields):
    return UserDatabase.get_properties(user_id, fields)


def get_customs(user_id):
    fields = ['dnd', 'holiday_mode', 'language']
    customs = UserDatabase.get_properties(user_id, fields)

    return customs['dnd'], customs['holiday_mode'], customs['language']
