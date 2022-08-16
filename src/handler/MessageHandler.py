'''
        MessageHandler module, as you can understand from the name,
        handles the messages sent by user. Just like CommandHandler module,
        Telegram API also has a same named module.

        Hacettepe Duyurucusu is interested in messages for subscriptions' sake.
        If the user write a department's name and sends it, bot controls the
        subscription status and decides whether to subscribe or unsubscribe.
        
        For the simplicity, bot doesn't require user to write one by one those
        departments. That's where Keyboard module comes in. The difference
        between normal and inline buttons is that normal ones are being used
        just because of reduce time waste. I mean when you click them, they don't
        send any data or they don't have any listener. Telegram App simply
        copy-paste-sends the text inside of them.
'''



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

    else:
        message = Text.encode('invalid-message', language)
        update.message.reply_text(message)


def feedback_done(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    language = User.get_language(user_id)

    context.bot.forward_message(chat_id=config.feedback_chat_id,
                                from_chat_id=update.message.chat_id,
                                message_id=update.message.message_id)
    
    context.bot.send_message(chat_id=config.feedback_chat_id, text=user_id)

    message = Text.encode('feedback-done', language)
    update.message.reply_text(message)
    return ConversationHandler.END
    