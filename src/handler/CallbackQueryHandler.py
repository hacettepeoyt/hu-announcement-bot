'''
        When the user clicked to an inline button, Telegram sends
        a CallbackQuery to bot. This query includes data which we use
        to understand what to do with request.

        I used inline buttons in settings page. There are three of them.
        Main function decides what to do.

        There are other functions that aren't directly related with the
        handler. They are there because changing the language isn't
        one step procedure.
'''



import telegram
from telegram import Update
from telegram.ext import CallbackContext
import os
from src import User, Text
from src.Keyboard import create_inline_keyboard


def main(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    current_dnd, current_holiday, current_lang = User.get_customs(user_id)
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




def find_next_language(language):
    language_list = find_language_list()
    current_index = language_list.index(language)

    if current_index == (len(language_list) - 1):
        return language_list[0]

    return language_list[current_index + 1]
    

def find_language_list():
    '''
        Finds available languages from locale folder.
        This can be handled by storing a simple list that includes
        the languages, but adding a language becomes more tricky.
        Thanks to this function, we don't need to update that language list
        everytime we add a new language.
    '''


    file_list = sorted(os.listdir('locale/'))
    languages = []

    for file in file_list:
        if file[-4:] != 'json':
            continue

        name = file.replace('.json', '')
        languages.append(name)

    return languages
    