'''
        CommandHandler module handles the commands that sent by users.
        Telegram API has also module named CommandHandler, this is
        obviously different than that.

        I find this module most useful one, because using the commands
        at enduser side and handling them here is the easiest thing in the world.
        
        Function names are self explanatory. One thing to mention is that you see
        two similar line of codes in every method. Finding the language of the user
        and creating a proper message to that. Thanks to Text module which is in
        src/ , bot simply finds that proper message and reply to user.

        This module does not handle just user commands, it also handles admin commands.
        As a main developer and the owner of the project, I, sometimes need to send
        message to every user of Hacettepe Duyurucusu. Those messages are mostly
        related with the updates.
'''



import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from src import User, Text, Announcement
from scraper.index import availableDepartments
from src.Keyboard import create_keyboard, create_inline_keyboard
from src.Logging import logger
from config import admin_id


def start(update: Update, context: CallbackContext):
    User.enroll(update.effective_user)
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('greet', language)

    update.message.reply_text(message)


def help(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('help', language)

    update.message.reply_text(message)


def new_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('new-sub', language)

    subscriptions = User.get_subscriptions(update.effective_user.id)
    possible_deps = [department.name for department in availableDepartments.values() if
                     department.name not in subscriptions]

    reply_markup = create_keyboard(possible_deps, language)
    update.message.reply_text(message, reply_markup=reply_markup)


def remove_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('remove-sub', language)

    subscriptions = User.get_subscriptions(update.effective_user.id)
    reply_markup = create_keyboard(subscriptions, language)
    update.message.reply_text(message, reply_markup=reply_markup)


def reset_subscriptions(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('reset-sub', language)

    User.reset_subscriptions(update.effective_user.id)
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())


def settings(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    dnd, holiday, lang = User.get_customs(user_id)

    message = Text.get_settings(dnd, holiday, lang)
    reply_markup = create_inline_keyboard(language)
    update.message.reply_text(message, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def donate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)

    message = Text.encode('donation', language)
    update.message.reply_text(message, parse_mode=telegram.ParseMode.HTML)


def feedback(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('feedback-info', language)

    update.message.reply_text(message)
    return 1


def cancel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    message = Text.encode('cancel', language)

    update.message.reply_text(message)
    return ConversationHandler.END


def answer_feedback(update: Update, context: CallbackContext):
    reciever_id = update.message.reply_to_message.forward_from.id
    message = update.message.text[8:]
    context.bot.send_message(chat_id=reciever_id, text=message,
                             parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


def add_new_department(update: Update, context: CallbackContext):
    is_admin = update.effective_user.id == admin_id

    if is_admin:
        Announcement.new_department(context.args[0])
    else:
        update.message.reply_text("403")


def send_from_admin(update: Update, context: CallbackContext):
    message = update.message.text[16:]

    if update.effective_user.id == admin_id:
        for user in User.get_all_users():
            try:
                context.bot.send_message(chat_id=user, text=message,
                                         parse_mode=telegram.ParseMode.HTML,
                                         disable_web_page_preview=True)
                logger.info(f"Admin sent a message to {user}")

            except telegram.error.Unauthorized:
                logger.info(f"Couldn't deliver message to {user}")
    else:
        update.message.reply_text("403")
        