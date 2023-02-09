import html
import json
import traceback
from typing import Union

import telegram.constants
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import ContextTypes

from .app import logger, USER_DB, LOCALE_DEPARTMENT_MAP, decode, get_possible_deps
from .config import ADMIN_ID, FEEDBACK_CHAT_ID, LOGGER_CHAT_ID, DEFAULT_DEPS
from .utils import find_next_language


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)

    if not user:
        user = await USER_DB.new_user(user_id, update.effective_user.first_name, update.effective_user.last_name,
                                      DEFAULT_DEPS)

    message = decode('cmd-start', user['language'])
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=ReplyKeyboardRemove())


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    message = decode('cmd-help', user['language'])
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=ReplyKeyboardRemove())


async def new_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    possible_deps = get_possible_deps(user['departments'])
    reply_markup = create_keyboard(possible_deps, user['language'])

    if possible_deps:
        message = decode('cmd-add', user['language'])
    else:
        message = decode('full-subscription', user['language'])

    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)


async def remove_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    reply_markup = create_keyboard(user['departments'], user['language'])

    if user['departments']:
        message = decode('cmd-remove', user['language'])
    else:
        message = decode('empty-subscription', user['language'])

    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)


async def reset_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)

    if not user['departments']:
        message = decode('empty-subscription', user['language'])
    else:
        await USER_DB.update_subscriptions(user_id, [])
        message = decode('cmd-reset', user['language'])

    await context.bot.send_message(chat_id=user_id, text=message)


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    reply_markup = create_inline_keyboard(user['language'])
    message = get_settings(user['dnd'], user['holiday_mode'], user['language'])
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup,
                                   parse_mode=telegram.constants.ParseMode.HTML)


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    message = decode('cmd-feedback', user['language'])
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=ReplyKeyboardRemove())
    return 1


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    message = decode('cmd-cancel', user['language'])
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=ReplyKeyboardRemove())
    return -1


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    message = decode('cmd-donate', user['language'])
    await context.bot.send_message(chat_id=update.effective_user.id, text=message,
                                   parse_mode=telegram.constants.ParseMode.HTML)


async def admin_announcement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    language = user['language']

    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text=decode('auth-fail', language))
        return

    # Message: /<command> <message> --- ignore "/<command>" text, accept only <message> part.
    admin_message = ' '.join(update.message.text.split()[1:])
    for target in await USER_DB.find_all():
        try:
            context.bot.send_message(chat_id=target, text=admin_message,
                                     parse_mode=telegram.constants.ParseMode.HTML)
            logger.info(f"Message has been sent to {target}")
        except telegram.error.Forbidden:
            logger.info(f"FORBIDDEN: Message couldn't be delivered to {target}")

    message = decode('admin-announcement-successful', language)
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=ReplyKeyboardRemove())


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)

    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text=decode('auth-fail', user['language']))
        return

    receiver_id = context.args[0]
    answer_msg = " ".join(update.message.text.split()[2:])
    answer_msg = answer_msg.replace('/answer', '').replace(receiver_id, '').strip()
    message = decode('admin-answer-success', user['language'])
    await context.bot.send_message(chat_id=receiver_id, text=answer_msg, parse_mode=telegram.constants.ParseMode.HTML,
                                   disable_web_page_preview=True)
    await context.bot.send_message(chat_id=FEEDBACK_CHAT_ID, text=message)


async def settings_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    query = update.callback_query
    data = query.data

    if data == 'settings-dnd-btn':
        await USER_DB.toggle_dnd(user_id)
        user['dnd'] = not user['dnd']
    elif data == 'settings-holiday-mode-btn':
        await USER_DB.toggle_holiday_mode(user_id)
        user['holiday_mode'] = not user['holiday_mode']
    elif data == 'settings-language-btn':
        user['language'] = find_next_language(user['language'])
        await USER_DB.toggle_language(user_id, user['language'])

    message = get_settings(user['dnd'], user['holiday_mode'], user['language'])
    reply_markup = create_inline_keyboard(user['language'])
    await query.answer(text=decode('settings-success', user['language']))
    await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def update_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    department_name = update.message.text
    subscriptions = user['departments']
    language = user['language']

    if department_name not in LOCALE_DEPARTMENT_MAP[language]:
        await context.bot.send_message(chat_id=user_id, text=decode('department-doesnt-exist', language))
        return

    chosen_department_code = LOCALE_DEPARTMENT_MAP[language][department_name]

    if chosen_department_code in subscriptions:
        subscriptions.remove(chosen_department_code)
        reply_markup = create_keyboard(subscriptions, language)
        message = f"{decode('unsubscribe-success', language)} {department_name}"
    else:
        subscriptions.append(chosen_department_code)
        possible_deps = get_possible_deps(subscriptions)
        reply_markup = create_keyboard(possible_deps, language)
        message = f"{decode('subscribe-success', language)} {department_name}"

    await USER_DB.update_subscriptions(user_id, subscriptions)
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)


async def feedback_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user = await USER_DB.find(user_id)
    message = decode('feedback-done', user['language'])
    await context.bot.forward_message(chat_id=FEEDBACK_CHAT_ID, from_chat_id=user_id,
                                      message_id=update.message.message_id)
    await context.bot.send_message(chat_id=FEEDBACK_CHAT_ID, text=user_id)
    await context.bot.send_message(chat_id=user_id, text=message)
    return -1


async def err_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""

    """
    Below code belongs to python-telegram-bot examples.
    Url: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py
    """
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096-character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.HTML)


# UTILS

# The key function in sort() doesn't take extra argument, that's why I used this temp variable.
temp_language_var: str = ''


def create_keyboard(_list: list[str], language: str) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
    """
    Takes a list, decodes and sort them in given language
    (sorting is being made according to given language's CHARS value). After that,
    creates a reply keyboard markup. In case the list is empty,
    returns ReplyKeyboardRemove.
    :param _list: List that contains department ids (doesn't have to be department ids)
    :param language: Language of the buttons
    :return: If the _list is empty ReplyKeyboardRemove, otherwise ReplyKeyboardMarkup
    """
    global temp_language_var

    if not _list:
        return ReplyKeyboardRemove()

    temp_language_var = language
    decoded_list = [decode(elem, language) for elem in _list]
    decoded_list.sort(key=custom_sorting_key)
    buttons = [[KeyboardButton(elem)] for elem in decoded_list]
    return ReplyKeyboardMarkup(buttons)


def custom_sorting_key(text: str) -> list[int]:
    """
    A language specific sorting key generator.
    :param text: The input record
    :return: List of each char's index number
    """
    global temp_language_var
    chars = decode('CHARS', temp_language_var)
    return [chars.index(text[i]) for i in range(len(text))]


def create_inline_keyboard(language: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup in given language.
    :param language: Language of the buttons
    :return: InlineKeyboardMarkup that contains settings buttons
    """

    buttons = []
    button_types = ['settings-dnd-btn', 'settings-holiday-mode-btn', 'settings-language-btn']
    for _type in button_types:
        buttons.append([InlineKeyboardButton(decode(_type, language), callback_data=_type)])
    return InlineKeyboardMarkup(buttons)


def get_settings(dnd: bool, holiday_mode: bool, language: str) -> str:
    """
    Generates a user specific settings page message.
    :param dnd: Do not disturb status
    :param holiday_mode: Holiday mode status
    :param language: Language of the message
    :return: Settings page message
    """

    text = ""

    if dnd:
        text += f"\U0001F508 <b>{decode('dnd-text', language)}:</b> {decode('enabled-text', language)}\n\n"
    else:
        text += f"\U0001F508 <b>{decode('dnd-text', language)}:</b> {decode('disabled-text', language)}\n\n"

    if holiday_mode:
        text += f"\U0001F3D6 <b>{decode('holiday-mode-text', language)}:</b> {decode('enabled-text', language)}\n\n"
    else:
        text += f"\U0001F3D6 <b>{decode('holiday-mode-text', language)}:</b> {decode('disabled-text', language)}\n\n"

    text += f"\U0001F30D <b>{decode('language-text', language)}:</b> {decode('language', language)}\n\n\n"

    text += f"<b>{decode('dnd-text', language)}:</b> <i>{decode('dnd-description', language)}</i>\n\n" \
            f"<b>{decode('holiday-mode-text', language)}:</b> <i>{decode('holiday-mode-description', language)}</i>\n"
    return text
