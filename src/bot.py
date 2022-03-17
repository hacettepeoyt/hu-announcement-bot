import logging

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import MessageHandler as Mh
import AnnouncementHandler as Ah
import User
import config
from database import UserDatabase
from scraper.chemie import Chemie
from scraper.cs import ComputerScience
from scraper.ie import IndustrialEngineering
from scraper.math import Math
from scraper.medicine import Medicine
from scraper.sksdb import Sksdb
from scraper.stat import Stat
from scraper.tomer import Tomer

'''
In bot module, I've written the core code. Think this module as the Eiffel Tower.
You can go anywhere in the city from here.

We're enabling logging in the first lines. After that, there are objects which I created them from scraper module.
You're seeing long <from scraper.department import department> formatted imports, yeah that's why. Some Python problems...
After that, I'm adding those department object into a dictionary called departments{}.

Later on, there are some functions to call whenever the user invokes.
start() --> User will user this to start to bot. There is welcome message and database checking. If the user isn't in database,
mongodb will add.
help() --> This is for giving some basic information about how to use bot.
is_online() --> This is for checking the bot if she is online or not (yes, she..).
main() --> Core function. Polling is written here.
'''

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

    update.message.reply_text(f"Hi {update.effective_user.first_name}! See /help to learn how to use \n\n")

    UserDatabase.add_user(update.effective_user.id,update.effective_user.first_name,update.effective_user.last_name)


def help(update: Update, context: CallbackContext):

    update.message.reply_text(text="See the menu for commands, let me give you hint\n\n"
                                   "/add   --->   You can subscribe to available departments with this command\n"
                                   "/remove   --->   You can unsubscribe from departments with this command\n\n",
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def is_online(update: Update, context: CallbackContext):

    update.message.reply_text("Yes, I'm alive right now!")


def main():

    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start)),
    dispatcher.add_handler(CommandHandler('online_status', is_online))
    dispatcher.add_handler(CommandHandler('remove', User.remove_subscription))
    dispatcher.add_handler(CommandHandler('add', User.add_subscription))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, Mh.main))

    updater.job_queue.run_repeating(Ah.check_new_announcements, interval=600, first=10)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
