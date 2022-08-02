from mongo import AnnouncementDatabase
from scraper.index import availableDepartments


def check_new_announcements():
    document_list = AnnouncementDatabase.find_all()

    for old_document in document_list:
        department_id = old_document['department']
        print(f"Checking {department_id}...")

        new_announcements = availableDepartments[department_id].get_announcements()
        diff = compare(old_document['announcements'], new_announcements)

        if diff:
            AnnouncementDatabase.update(old_document['department'], new_announcements)


def compare(olds, news):
    diff = []

    for announcement in news:
        if announcement not in olds:
            diff.append(announcement)

    return diff
