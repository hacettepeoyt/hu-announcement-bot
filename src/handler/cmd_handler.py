'''
        CommandHandler module handles the commands that sent by users.
        Telegram API has also module named CommandHandler, this is
        obviously different than that.

        I find this module most useful one, because using the commands
        at enduser side and handling them here is the easiest thing in the world.
        
        Function names are self explanatory. One thing to mention is that you see
        two similar line of codes in every method. Finding the language of the user
        and creating a proper message to that. Thanks to text module which is in
        src/ , bot simply finds that proper message and reply to user.

        This module does not handle just user commands, it also handles admin commands.
        As a main developer and the owner of the project, I, sometimes need to send
        message to every user of Hacettepe Duyurucusu. Those messages are mostly
        related with the updates.
'''



import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from .. import user, text, announcement
from ..scraper.index import availableDepartments
from ..keyboard import create_keyboard, create_inline_keyboard
from ..logging import logger
from config import feedback_chat_id


def start(update: Update, context: CallbackContext):
    user.enroll(update.effective_user)
    user_id = update.effective_user.id
    language = user.get_language(user_id)
    message = text.encode('greet', language)

    update.message.reply_text(message)


def help(ctx):
    language = ctx.author.get_language()
    message = text.encode('help', language)

    ctx.send(message)


def new_subscription(ctx):
    language = ctx.author.get_language()
    subscriptions = user.get_subscriptions(update.effective_user.id)

    possible_deps = [department.name for department in availableDepartments.values() if
                     department.name not in subscriptions]


    if len(possible_deps) == 0:
        message = text.encode('full-subscription', language)
    else:
        message = text.encode('new-sub', language)

    if ctx.backend == 'telegram':
        reply_markup = create_keyboard(possible_deps, language)
        ctx.send(message, reply_markup=reply_markup)
    else:
        ctx.send(message)


def remove_subscription(ctx):
    language = ctx.author.get_language()
    subscriptions = ctx.author.get_subscriptions()

    if len(subscriptions) == 0:
        message = text.encode('empty-subscription', language)
    else:
        message = text.encode('remove-sub', language)

    if ctx.backend == "telegram":
        reply_markup = create_keyboard(subscriptions, language)
        ctx.send(message, reply_markup=reply_markup)
    else:
        ctx.send(message)


def reset_subscriptions(ctx):
    language = ctx.author.get_language()
    message = text.encode('reset-sub', language)

    ctx.author.reset_subscriptions()
    if ctx.backend == "telegram":
        ctx.send(message, reply_markup=ReplyKeyboardRemove())
    else:
        ctx.send(message)


def settings(ctx):
    lang = ctx.author.get_language()
    dnd = ctx.author.get_dnd()
    holiday = ctx.author.get_holiday_mode()

    message = text.get_settings(dnd, holiday, lang)
    if ctx.backend == 'telegram':
        reply_markup = create_inline_keyboard(language)
        ctx.send(message, reply_markup=reply_markup, parse_mode='HTML')
    else:
        ctx.send(message)


def donate(ctx):
    language = ctx.author.get_language()

    message = text.encode('donation', language)
    ctx.send(message, parse_mode='HTML')


def feedback(ctx):
    language = ctx.author.get_language()
    message = text.encode('feedback-info', language)

    ctx.send(message)
    ctx.wait_for()  # TODO: implement this.


def cancel(ctx):
    language = ctx.author.get_language()
    message = text.encode('cancel', language)

    ctx.send(message)


def answer_feedback(ctx, receiver_id: int, answer: str):
    ctx.bot.get_user(ctx.backend, receiver_id).send(answer, parse_mode="HTML", disable_web_page_preview=True)


def add_new_department(ctx, department: str):
    # TODO: is_admin decorator
    if ctx.author != ctx.get_admin():
        ctx.send("You do not have enough permissions to run this command.")
        return

    announcement.new_department(department)
    ctx.send("200")


def send_from_admin(ctx, message: str):
    # TODO: is_admin decorator
    if ctx.author != ctx.get_admin():
        ctx.send("You do not have enough permissions to run this command.")
        return

    for backend, user_id in user.get_all_users():
        try:
            ctx.bot.get_user(backend, user_id).send(message, parse_mode='HTML', disable_web_page_preview=True)
            logger.info(f"Admin sent a message to {user_id}")
        except Exception:  # FIXME: better exc support.
            logger.info(f"Couldn't deliver message to {user_id}")
        
