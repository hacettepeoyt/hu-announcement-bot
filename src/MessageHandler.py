from telegram import Update
from telegram.ext import CallbackContext

import User
import config
from database import UserDatabase


def main(update: Update, context: CallbackContext):

    process = update.message.text.split()[0]
    departmentName = ' '.join(update.message.text.split()[1:])

    if process == 'Add':
        subscriptions = UserDatabase.find_subscriptions(update.effective_user.id)
        if departmentName not in subscriptions:
            subscriptions.append(departmentName)
            UserDatabase.update_subscriptions(update.effective_user.id, subscriptions)
            update.message.reply_text(f"Successfully subscribed to {departmentName} Department!")
        else:
            update.message.reply_text(f"You are already subscribed to {departmentName} Department!")

        User.add_subscription(update,context)                # This is for updating the buttons in screen

    if process == 'Remove':
        subscriptions = UserDatabase.find_subscriptions(update.effective_user.id)
        if departmentName in subscriptions:
            subscriptions.remove(departmentName)
            UserDatabase.update_subscriptions(update.effective_user.id, subscriptions)
            update.message.reply_text(f"Successfully unsubscribed from {departmentName} Department!")
        else:
            update.message.reply_text(f"You are not subscribed to {departmentName} Department!")

        User.remove_subscription(update, context)            # This is for updating the buttons in screen

    if update.message.text == 'Thank you Hacettepe Duyurucusu!':
        update.message.reply_text("You are welcome sweethart :)")


def send_from_admin(update: Update, context: CallbackContext):

    message_from_admin = ' '.join(context.args[:])

    if update.effective_user.id == config.admin_id:
        all_users = UserDatabase.find_all_users()

        for user in all_users:

            try:
                context.bot.send_message(chat_id=user, text=message_from_admin)
                print(f"Admin sent a message to {user}")

            except telegram.error.Unauthorized:
                print(f"I couldn't deliver message to {user}")
    else:
        context.bot.send_message(chat_id=update.effective_user, text='Oops! You are not admin. Sshhh!')
