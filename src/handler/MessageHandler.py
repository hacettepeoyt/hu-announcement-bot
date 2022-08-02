from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

import config
from scraper.index import availableDepartments
from src import Text, User
from src.Keyboard import create_keyboard


def edit_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)

    text = update.message.text
    departments = Text.get_departments(language)

    if text in departments:
        department_id = departments[text]
        subscriptions = User.get_subscriptions(user_id)

        if department_id in subscriptions:
            subscriptions = User.remove_subscription(user_id, department_id)
            reply_markup = create_keyboard(subscriptions, language)

            update.message.reply_text(f"{Text.encode('unsub-success', language)} "
                                      f"{Text.encode(department_id, language)}",
                                      reply_markup=reply_markup)

        else:
            subscriptions = User.add_subscription(user_id, department_id)
            possible_subs = [department.name for department in availableDepartments.values()
                             if department.name not in subscriptions]

            reply_markup = create_keyboard(possible_subs, language)

            update.message.reply_text(f"{Text.encode('sub-success', language)} "
                                      f"{Text.encode(department_id, language)}",
                                      reply_markup=reply_markup)


def feedback_done(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)

    context.bot.forward_message(chat_id=config.feedback_chat_id,
                                from_chat_id=update.message.chat_id,
                                message_id=update.message.message_id)

    message = Text.encode('feedback-done', language)
    update.message.reply_text(message)
    return ConversationHandler.END
