'''
        There are two types of Keyboards in Telegram.
        This module helps us to create inline and normal buttons for
        those keyboards. Buttons have their text on them, so text module goes brrrr
'''



from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

from . import text


def create_keyboard(array, language):
    if len(array) == 0:
        return ReplyKeyboardRemove()

    deps = [text.encode(dep_id, language) for dep_id in array]
    deps.sort()
    buttons = [[KeyboardButton(dep)] for dep in deps]

    return ReplyKeyboardMarkup(buttons)


def create_inline_keyboard(language):
    buttons = []
    types = ['dnd-btn', 'holiday-btn', 'language-btn']

    for type in types:
        text = text.encode(type, language)
        buttons.append([InlineKeyboardButton(text=text, callback_data=type)])

    return InlineKeyboardMarkup(buttons)
    
