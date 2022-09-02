'''
        I mentioned that bot has one job to execute regularly. Task module
        represents the jobs. Since the main task (checking announcements and then
        notifying user and then updating database) is really long to implement,
        it deserves it's own module.

        Also, for the future it would be nice to have it. Maybe new tasks can
        be added.
'''


from . import announcement, text, user
from .logging import logger
from .scraper.index import availableDepartments
from . import abc


def check_announcements(bot):
    for department in availableDepartments.values():
        logger.info(f"Checking {department.name}...")

        try:
            news = department.get_announcements()
        except:
            logger.info(f"Couldn't connect to {department.name}!")
            continue

        olds = announcement.find(department.name)
        diff = announcement.compare(olds, news)

        users: list[abc.User] = []
        for id_, backend in user.get_subscribers(department.name):
            users.append(bot.get_user(backend, user_id=id_))

        for ann in diff:
            notify_users(ann, users, department.name)

        if diff:
            olds.extend(diff)
            announcement.update(department.name, olds)


def notify_users(announcement, users: list[abc.User], department_id):
    for user in users:
        language = user.get_language()
        message = text.create_announcement_text(department_id, announcement, language)

        try:
            user.send(message, parse_mode='HTML',
                               disable_web_page_preview=True,
                               disable_notification=user.get_dnd())

            logger.info(f"Message has been sent to {user} from {department_id} Department")

        except Exception:  # TODO: Proper exception support.
            logger.info(f"Couldn't deliver message to {user}")
            
