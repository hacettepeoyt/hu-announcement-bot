from mongo import AnnouncementDatabase


def find(department_id):
    return AnnouncementDatabase.find(department_id)


def compare(olds, news):
    diff = []

    for announcement in news:
        if announcement not in olds:
            diff.append(announcement)

    return diff