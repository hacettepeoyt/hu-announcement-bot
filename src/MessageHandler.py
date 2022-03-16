from telegram import Update
from telegram.ext import CallbackContext

import User
from database import UserDatabase


def main(update: Update, context: CallbackContext):

    process = update.message.text.split()[0]
    departmentName = update.message.text.split()[1]

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