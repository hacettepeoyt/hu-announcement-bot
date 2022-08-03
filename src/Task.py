import telegram
from telegram.ext import CallbackContext

import Announcement
import Text
import User
from Logging import logger
from scraper.index import availableDepartments


def check_announcements(context: CallbackContext):
    for department in availableDepartments.values():
        logger.info(f"Checking {department.name}...")

        try:
            news = department.get_announcements()
        except:
            logger.info(f"Couldn't connect to {department.name}!")
            continue

        olds = Announcement.find(department.name)
        diff = Announcement.compare(olds, news)
        user_list = User.get_subscribers(department.name)

        for announcement in diff:
            notify_users(context, announcement, user_list, department.name)

        if diff:
            Announcement.update(department.name, news)


def notify_users(context: CallbackContext, announcement, user_list, department_id):
    for user in user_list:
        language = User.get_language(user)
        message = Text.create_announcement_text(department_id, announcement, language)

        try:
            context.bot.send_message(chat_id=user, text=f"{message}",
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)

            logger.info(f"Message has been sent to {user} from {department_id} Department")

        except telegram.error.Unauthorized:
            logger.info(f"Couldn't deliver message to {user}")
