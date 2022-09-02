'''
        Announcement module is created by the sake of abstraction.
        I write about this abstraction in mongo/announcement_db
'''



from .mongo import announcement_db
from .logging import logger


def find(department_id):
    return announcement_db.find(department_id)


def update(department_id, announcements):
    announcement_db.update(department_id, announcements)
    logger.info(f"Announcements updated for {department_id} department in database!")


def new_department(department_id):
    document = {
        'department': department_id,
        'announcements': []
    }

    announcement_db.insert_documents([document])
    logger.info('New document(s) have been inserted!')


def compare(olds, news):
    diff = []

    for announcement in news:
        if announcement not in olds:
            diff.append(announcement)

    return diff
    
