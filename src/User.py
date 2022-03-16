from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from database import UserDatabase
from bot import departments


def remove_subscription(update: Update, context: CallbackContext):

    subscribedDepartments = UserDatabase.find_subscriptions(update.effective_user.id)
    buttons = []
    thanksButton = [[KeyboardButton('Thank you Hacettepe Duyurucusu!')]]

    for department in subscribedDepartments:
        department = departments[department]
        buttons.append([KeyboardButton("Remove " + department.name)])

    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_user.id, text="You are already don't have subscriptions\n\n"
                                                                        "If you want a new department, please write a feedback!\n\n"
                                                                        "Also thank me ^^",
                                 reply_markup=ReplyKeyboardMarkup(thanksButton))
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text="Choose a department to unsubscribe from below",
                                 reply_markup=ReplyKeyboardMarkup(buttons))


def add_subscription(update: Update, context: CallbackContext):

    subscribedDepartments = UserDatabase.find_subscriptions(update.effective_user.id)
    unsubscribedDepartments = [department.name for department in departments.values() if department.name not in subscribedDepartments]
    buttons = []
    thanksButton = [[KeyboardButton('Thank you Hacettepe Duyurucusu!')]]

    for department in unsubscribedDepartments:
        department = departments[department]
        buttons.append([KeyboardButton("Add " + department.name)])

    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_user.id, text="You are already subscribed to all departments\n\n"
                                                                        "If you want a new department, please write a feedback!\n\n"
                                                                        "Also thank me ^^",
                                 reply_markup=ReplyKeyboardMarkup(thanksButton))
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text="Choose a department to subscribe from below",
                                 reply_markup=ReplyKeyboardMarkup(buttons))