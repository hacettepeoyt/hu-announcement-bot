'''
        CommandHandler module handles the commands that sent by users.
        Telegram API has also module named CommandHandler, this is
        obviously different than that.

        I find this module most useful one, because using the commands
        at enduser side and handling them here is the easiest thing in the world.
        
        Function names are self explanatory. One thing to mention is that you see
        two similar line of codes in every method. Finding the language of the user
        and creating a proper message to that. Thanks to text module which is in
        src/ , bot simply finds that proper message and reply to user.

        This module does not handle just user commands, it also handles admin commands.
        As a main developer and the owner of the project, I, sometimes need to send
        message to every user of Hacettepe Duyurucusu. Those messages are mostly
        related with the updates.
'''



import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from .. import user, text, announcement
from ..scraper.index import availableDepartments
from ..keyboard import create_keyboard, create_inline_keyboard
from ..logging import logger
from config import admin_id, feedback_chat_id


def start(update: Update, context: CallbackContext):
    user.enroll(update.effective_user)
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('greet', language)

    update.message.reply_text(message)


def help(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('help', language)

    update.message.reply_text(message)


def new_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    subscriptions = user.get_subscriptions(update.effective_user.id)

    possible_deps = [department.name for department in availableDepartments.values() if
                     department.name not in subscriptions]

    reply_markup = create_keyboard(possible_deps, language)

    if len(possible_deps) == 0:
        message = text.encode('full-subscription', language)
    else:
        message = text.encode('new-sub', language)

    update.message.reply_text(message, reply_markup=reply_markup)


def remove_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    subscriptions = user.get_subscriptions(update.effective_user.id)
    reply_markup = create_keyboard(subscriptions, language)

    if len(subscriptions) == 0:
        message = text.encode('empty-subscription', language)
    else:
        message = text.encode('remove-sub', language)

    update.message.reply_text(message, reply_markup=reply_markup)


def reset_subscriptions(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('reset-sub', language)

    user.reset_subscriptions(update.effective_user.id)
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())


def settings(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    dnd, holiday, lang = user.get_customs(user_id)

    message = text.get_settings(dnd, holiday, lang)
    reply_markup = create_inline_keyboard(language)
    update.message.reply_text(message, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def donate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)

    message = text.encode('donation', language)
    update.message.reply_text(message, parse_mode=telegram.ParseMode.HTML)


def feedback(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('feedback-info', language)

    update.message.reply_text(message)
    return 1


def cancel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('cancel', language)

    update.message.reply_text(message)
    return ConversationHandler.END


def answer_feedback(update: Update, context: CallbackContext):
    reciever_id = context.args[0]
    message = update.message.text
    message = message.replace('/answer', '').replace(reciever_id, '').strip()
    
    context.bot.send_message(chat_id=reciever_id, text=message,
                             parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)

    context.bot.send_message(chat_id=feedback_chat_id,
                             text="200")


def add_new_department(update: Update, context: CallbackContext):
    is_admin = update.effective_user.id == admin_id

    if is_admin:
        announcement.new_department(context.args[0])
        update.message.reply_text("200")
    else:
        update.message.reply_text("403")


def send_from_admin(update: Update, context: CallbackContext):
    message = update.message.text[16:]

    if update.effective_user.id == admin_id:
        for user_id in user.get_all_users():
            try:
                context.bot.send_message(chat_id=user_id, text=message,
                                         parse_mode=telegram.ParseMode.HTML,
                                         disable_web_page_preview=True)
                logger.info(f"Admin sent a message to {user}")

            except telegram.error.Unauthorized:
                logger.info(f"Couldn't deliver message to {user}")
    else:
        update.message.reply_text("403")
        
