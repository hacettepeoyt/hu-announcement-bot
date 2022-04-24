import datetime
import telegram
import requests
from telegram.ext import CallbackContext

from scraper.main import availableDepartments
from database import UserDatabase, AnnouncementDatabase

'''
In AnnouncementHandler module, code will check if there is a new announcement from departments.
Also, it will send the messages with send_message() function.

make_pretty() --> This is for preparing the text to send, because some of the announcements include
None values. The function will clear that. For instance, content might None if there is no content
but there are title and URL.
'''


def check_new_announcements(context: CallbackContext):

    for department in availableDepartments.values():
        print(f"Checking {department.name}...")

        try:
            new_announcement = department.get_announcement()
        except requests.exceptions.ConnectTimeout:
            print(f"Couldn't connect to {department.name}!")
            continue

        old_announcements = AnnouncementDatabase.find_announcement(department.name)

        if new_announcement != old_announcements:
            user_list = UserDatabase.find_subscribers(department.name)
            send_message(context, new_announcement, user_list, department.name)
            AnnouncementDatabase.update_announcements(department.name, new_announcement)


def send_message(context: CallbackContext, announcement, userList, department_name):

    text_to_print = make_pretty(department_name, announcement)

    for user in userList:

        try:
            context.bot.send_message(chat_id=user, text=f"{text_to_print}",
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)

            print(f"Message has been sent to {user} from {department_name} Department at {datetime.datetime.now()} GMT")

        except telegram.error.Unauthorized:
            print(f"I couldn't deliver message to {user}")


def make_pretty(department_name, announcement):

    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    text = f'<b>Hey, there is a message from {department_name} Department!</b> \n\n'

    # This loop will eliminate the None values before printing. Especially content values might be None.
    for key in announcement.keys():
        if key == 'title' and title is not None:
            text += f"\U0001F514 <b>{title}</b>\n\n"
        if key == 'content' and content is not None:
            text += f"\U0001F4AC {content}\n\n"
        if key == 'url' and url is not None:
            text += f'\U0001F310 <a href="{url}">Details are here!</a>'

    return text
