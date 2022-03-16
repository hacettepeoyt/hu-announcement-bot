import logging

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import MessageHandler as Mh
import User
import config
from database import UserDatabase, AnnouncementDatabase
from scraper.chemie import Chemie
from scraper.cs import ComputerScience
from scraper.ie import IndustrialEngineering
from scraper.math import Math
from scraper.medicine import Medicine
from scraper.sksdb import Sksdb
from scraper.stat import Stat
from scraper.tomer import Tomer



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

math_website = Math()
sksdb_website = Sksdb()
chemie_website = Chemie()
cs_website = ComputerScience()
ie_website = IndustrialEngineering()
tomer_website = Tomer()
medicine_website = Medicine()
stat_website = Stat()

departments = {
    'CS': cs_website,
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website,
    'IE': ie_website,
    'TOMER': tomer_website,
    'Medicine': medicine_website,
    'Stat': stat_website
}


def start(update: Update, context: CallbackContext):

    update.message.reply_text(f"Hi {update.effective_user.name}! See /help to learn how to use \n\n")

    # Add the user into database if she/he isn't in yet!
    UserDatabase.add_user(update.effective_user.id)


def help(update: Update, context: CallbackContext):

    update.message.reply_text(text="See the menu for commands, let me give you hint\n\n"
                                   "/add   --->   You can subscribe to available departments with this command\n"
                                   "/remove   --->   You can unsubscribe from departments with this command\n\n",
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def is_online(update: Update, context: CallbackContext):

    update.message.reply_text("Yes, I'm alive right now!")


def check_new_announcements(context: CallbackContext):

    for department in departments.values():
        new_announcement = department.get_announcement()
        old_announcements = AnnouncementDatabase.find_announcement(department.name)

        if new_announcement != old_announcements:
            user_list = UserDatabase.find_subscribers(department.name)
            send_message(context, new_announcement, user_list, department.name)
            AnnouncementDatabase.update_announcements(department.name, new_announcement)


def send_message(context: CallbackContext, announcement, userList, department_name):

    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    text_to_print = f'<b>Hey, there is a message from {department_name} Department!</b> \n\n'

    # This loop will eliminate the None values before printing. Especially content values might be None.
    for key in announcement.keys():
        if key == 'title' and title is not None:
            text_to_print += f"\U0001F514 <b>{title}</b>\n\n"
        if key == 'content' and content is not None:
            text_to_print += f"\U0001F4AC {content}\n\n"
        if key == 'url' and url is not None:
            text_to_print += f'\U0001F310 <a href="{url}">Click here!</a>'

    for user in userList:
        context.bot.send_message(chat_id=user, text=f"{text_to_print}",
                                 parse_mode=telegram.ParseMode.HTML,
                                 disable_web_page_preview=True)

        print(f"Message has been sent to {user} from {department_name} Department!")


def main():

    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start)),
    dispatcher.add_handler(CommandHandler('online_status', is_online))
    dispatcher.add_handler(CommandHandler('remove', User.remove_subscription))
    dispatcher.add_handler(CommandHandler('add', User.add_subscription))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, Mh.main))

    updater.job_queue.run_repeating(check_new_announcements, interval=600, first=60)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
