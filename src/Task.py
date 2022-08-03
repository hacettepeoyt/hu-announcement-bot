import datetime

import requests
import telegram
from telegram.ext import CallbackContext

from scraper.index import availableDepartments
import User
import Announcement
import Text


def check_announcements(context: CallbackContext):
    for department in availableDepartments.values():
        print(f"Checking {department.name}...")

        try:
            news = department.get_announcements()
        except requests.exceptions.ConnectTimeout:
            print(f"Couldn't connect to {department.name}!")
            continue

        olds = Announcement.find(department.name)
        diff = Announcement.compare(olds, news)
        user_list = User.find_subscribers(department.name)

        for announcement in diff:
            notify_users(context, announcement, user_list, department.name)


def notify_users(context: CallbackContext, announcement, user_list, department_id):
    for user in user_list:
        language = User.get_language(user)
        message = Text.create_announcement_text(department_id, announcement, language)

        try:
            context.bot.send_message(chat_id=user, text=f"{message}",
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)

            print(f"Message has been sent to {user} from {department_id} Department at {datetime.datetime.now()} GMT")

        except telegram.error.Unauthorized:
            print(f"I couldn't deliver message to {user}")
