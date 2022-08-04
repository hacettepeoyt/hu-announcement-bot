import telegram
from telegram import Update
from telegram.ext import CallbackContext
import os
from src import User, Text
from src.Keyboard import create_inline_keyboard


def button(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    current_lang = User.get_language(user_id)
    current_dnd = User.get_dnd(user_id)
    current_holiday = User.get_holiday_mode(user_id)

    query = update.callback_query
    data = query.data

    if data == 'dnd-btn':
        current_dnd = not current_dnd
        User.set_dnd(user_id, current_dnd)

    elif data == 'holiday-btn':
        current_holiday = not current_holiday
        User.set_holiday_mode(user_id, current_holiday)

    elif data == 'language-btn':
        current_lang = find_next_language(current_lang)
        User.set_language(user_id, current_lang)

    query.answer()
    message = Text.get_settings(current_dnd, current_holiday, current_lang)
    reply_markup = create_inline_keyboard(current_lang)
    query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)


def find_language_list():
    file_list = sorted(os.listdir('src/locale/'))
    languages = []

    for file in file_list:
        name = file.replace('.json', '')
        languages.append(name)

    return languages


def find_next_language(language):
    language_list = find_language_list()
    current_index = language_list.index(language)

    if current_index == (len(language_list) - 1):
        return language_list[0]

    return language_list[current_index + 1]
