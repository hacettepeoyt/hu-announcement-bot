from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

import Text


def create_keyboard(array, language):
    if len(array) == 0:
        return ReplyKeyboardRemove()

    buttons = []

    for dep_id in array:
        dep_name = Text.encode(dep_id, language)
        buttons.append([KeyboardButton(dep_name)])

    return ReplyKeyboardMarkup(buttons)


def create_inline_keyboard(language):
    buttons = []
    types = ['dnd-btn', 'holiday-btn', 'language-btn']

    for type in types:
        text = Text.encode(type, language)
        buttons.append([InlineKeyboardButton(text=text, callback_data=type)])

    return InlineKeyboardMarkup(buttons)
