import logging

import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import config
from scraper.chemie import Chemie
from scraper.cs import ComputerScience
from scraper.math import Math
from scraper.sksdb import Sksdb



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

math_website = Math()
sksdb_website = Sksdb()
chemie_website = Chemie()
cs_website = ComputerScience()

websites = {
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website
}


def start(update: Update, context: CallbackContext):

    user = update.message.from_user
    user_name = user['first_name']
    print(user['id'])

    update.message.reply_text(f"Hi {user_name}! See /help to learn how to use \n\n"
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
                                  f"Available departments: {departments_text.strip(', ')}",
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


def remove_subscription(update: Update, context: CallbackContext):

    unsubscribedDepartments = find_subscribedWebsites(update.effective_user.id)
    buttons = []

    for department in unsubscribedDepartments:
        buttons.append([KeyboardButton("Remove " + department.name)])

    context.bot.send_message(chat_id=update.effective_user.id, text="Choose a department to unsubscribe from below",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def add_subscription(update: Update, context: CallbackContext):

    unsubscribedDepartments = find_unsubscribedWebsites(update.effective_user.id)
    buttons = []

    for department in unsubscribedDepartments:
        buttons.append([KeyboardButton("Add " + department.name)])

    context.bot.send_message(chat_id=update.effective_user.id, text="Choose a department to subscribe from below",
                             reply_markup=ReplyKeyboardMarkup(buttons))


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
        context.bot.send_message(chat_id=user, text=f"<b>Hey, there is a message from {website_name} Department!</b> \n\n"
                                                    f"{text_to_print}",
                                 parse_mode=telegram.ParseMode.HTML,
                                 disable_web_page_preview=True)


def messageHandler(update: Update, context: CallbackContext):

    process = update.message.text.split()[0]
    departmentName = update.message.text.split()[1]

    if process == 'Add':
        department = websites[departmentName]
        department.add_subscriber(update.effective_user.id)

    if process == 'Remove':
        department = websites[departmentName]
        department.remove_subscriber(update.effective_user.id)


def find_subscribedWebsites(user_id):

    subscribedDepartments = []

    for website in websites.values():
        if user_id in website.subscribers:
            subscribedDepartments.append(website)

    return subscribedDepartments


def find_unsubscribedWebsites(user_id):

    unsubscribedDepartments = []

    for website in websites.values():
        if user_id not in website.subscribers:
            unsubscribedDepartments.append(website)

    return unsubscribedDepartments


def main():

    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("online_status", isOnline))
    dispatcher.add_handler(CommandHandler("remove", remove_subscription))
    dispatcher.add_handler(CommandHandler("add", add_subscription))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

    updater.job_queue.run_repeating(check_newAnnouncements, interval=600, first=10)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
