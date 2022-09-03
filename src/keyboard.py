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
    types = ['/dnd', '/holiday', '/language']

    for type in types:
        button = InlineKeyboardButton(text=text.encode(type, language), callback_data=type)
        buttons.append([button])

    return InlineKeyboardMarkup(buttons)

