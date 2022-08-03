from mongo import AnnouncementDatabase
from Logging import logger


def find(department_id):
    return AnnouncementDatabase.find(department_id)


def update(department_id, announcements):
    AnnouncementDatabase.update(department_id, announcements)
    logger.info(f"Announcements updated for {department_id} department in database!")


def new_department(document):
    AnnouncementDatabase.insert_documents(document)
    logger.info('New document(s) have been inserted!')


def compare(olds, news):
    diff = []

    for announcement in news:
        if announcement not in olds:
            diff.append(announcement)

    return diff
