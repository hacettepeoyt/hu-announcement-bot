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


def get_subscribers(department_id):
    return user_db.find_subscribers(department_id)


def get_all_users():
    return user_db.find_all_users()
    
