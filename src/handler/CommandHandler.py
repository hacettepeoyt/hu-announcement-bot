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

    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    User.reset_subscriptions(update.effective_user.id)


def settings(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)
    dnd, holiday, lang = User.get_customs(user_id)

    message = Text.get_settings(dnd, holiday, lang)
    reply_markup = create_inline_keyboard(language)
    update.message.reply_text(message, reply_markup=reply_markup)


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
    context.bot.send_message(chat_id=reciever_id, text=message)


def add_new_department(update: Update, context: CallbackContext):
    is_admin = update.effective_user.id == admin_id

    if is_admin:
        Announcement.new_department(context.args[0])
    else:
        update.message.reply_text("403")


def send_from_admin(update: Update, context: CallbackContext):
    message_from_admin = ' '.join(context.args[:])

    if update.effective_user.id == admin_id:
        for user in User.get_all_users():
            try:
                context.bot.send_message(chat_id=user, text=message_from_admin)
                logger.info(f"Admin sent a message to {user}")

            except telegram.error.Unauthorized:
                logger.info(f"Couldn't deliver message to {user}")
    else:
        update.message.reply_text("403")
