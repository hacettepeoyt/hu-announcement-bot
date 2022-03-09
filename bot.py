import telegram
import config
import logging
import scraper

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

math_website = scraper.Math()
sksdb_website = scraper.Sksdb()
chemie_website = scraper.Chemie()
cs_website = scraper.ComputerScience()

websites = {
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website
}


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_name = user['first_name']
    print(user['id'])

    update.message.reply_text(f"Hi {user_name}! See /help to learn how to use \n"
                              f"By the way, you have been automatically subscribed to all departments!")

    for website in websites.values():
        website.add_subscriber(user['id'])


def help(update: Update, context: CallbackContext):
    user = update.message.from_user
    departments_text = ''
    for website in websites.values():
        departments_text += website.name + ', '

    context.bot.send_message(chat_id=user['id'],
                             text="If you want to subscribe a department, you should use /add command\n"
                                  "<i>Example:</i> <b>/add SKSDB</b> \n\n"
                                  "If you want to unsubscribe, you can use /remove command\n"
                                  "<i>Example:</i> <b>/remove SKSDB</b> \n\n"
                                  f"Current departments: {departments_text.strip(',')}",
                             parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


def isOnline(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user['id']

    context.bot.send_message(chat_id=user_id, text="Yes, I'm alive!")


def check_newAnnouncements(context: CallbackContext):
    for website in websites.values():
        announcement = website.get_announcement()

        if announcement is not None:
            subscribers = website.subscribers
            send_message(context, announcement, subscribers, website.name)


def remove_subscribtion(update: Update, context: CallbackContext):
    websiteName = context.args[0]
    user_id = update.message.from_user['id']
    website = websites[websiteName]
    website.remove_subscriber(user_id)


def add_subscribtion(update: Update, context: CallbackContext):
    websiteName = context.args[0]
    user_id = update.message.from_user['id']
    website = websites[websiteName]
    website.add_subscriber(user_id)


def send_message(context: CallbackContext, announcement, userList, website_name):
    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    text_to_print = ''

    # This loop will eliminate the None values before printing. Especially content values might be None.
    for key in announcement.keys():
        if key == 'title' and title is not None:
            text_to_print += f"\U0001F514 <b>{title}</b>\n\n"
        if key == 'content' and content is not None:
            text_to_print += f"\U0001F4AC {content}\n\n"
        if key == 'url' and url is not None:
            text_to_print += f'\U0001F310 <a href="{url}">Click here!</a>'

    for user in userList:
        context.bot.send_message(chat_id=user, text=f"<b>Announcement from {website_name} Department!!!</b> \n\n"
                                                    f"{text_to_print}",
                                 parse_mode=telegram.ParseMode.HTML,
                                 disable_web_page_preview=True)


def main():
    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("online_status", isOnline))
    dispatcher.add_handler(CommandHandler("remove", remove_subscribtion))
    dispatcher.add_handler(CommandHandler("add", add_subscribtion))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.job_queue.run_repeating(check_newAnnouncements, interval=600, first=10)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
