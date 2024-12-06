import traceback
from asyncio.exceptions import TimeoutError

import telegram
from aiohttp import ClientConnectorError, ConnectionTimeoutError
from telegram.ext import ContextTypes

from .app import logger, DEPARTMENT_DB, USER_DB, AVAILABLE_DEPARTMENTS, decode
from .config import LOGGER_CHAT_ID


async def check_announcements(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Checking for new announcements...")

    for department in AVAILABLE_DEPARTMENTS:
        logger.info(f"Checking {department.id}")
        dep = await DEPARTMENT_DB.find(department.id)

        if dep["is_active"] is False:
            message = f"Skipping {department.id}, because it's deactivated!"
            logger.info(message)
            await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, disable_notification=True)
            continue

        olds = dep["announcement_list"]

        try:
            news = await department.get_announcements()
        except ClientConnectorError:
            message = f"Connection Error while scraping {department.id}"
            logger.exception(message)
            await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, disable_notification=True)
            continue
        except (TimeoutError, ConnectionTimeoutError):
            message = f"Connection Timeout while scraping {department.id}"
            logger.exception(message)
            await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, disable_notification=True)
            continue
        # except TimeoutError:
        #     message = f"Connection Timeout while scraping {department.id}"
        #     logger.exception(message)
        #     await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, disable_notification=True)
        #     continue
        except:
            message = f"Undefined Error while scraping {department.id}"
            logger.exception(message)
            await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=f"{message}\n\n{traceback.format_exc()}")
            continue

        diff = compare(olds, news)

        if diff:
            olds.extend(diff)
            await DEPARTMENT_DB.update(department.id, olds)
            user_list = await USER_DB.get_subscribers(department.id)
            for announcement in diff:
                await notify_users(context, announcement, user_list, department.id)
            logger.info("New announcements have been inserted into database")


async def notify_users(context: ContextTypes.DEFAULT_TYPE, announcement: dict, user_list: list[dict],
                       department_id: str):
    for user in user_list:
        message = create_announcement_message(department_id, announcement, user['language'])

        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message, disable_notification=user['dnd'],
                                           parse_mode=telegram.constants.ParseMode.HTML, disable_web_page_preview=True)
            logger.info(f"Announcement has been sent to {user['user_id']}")
        except telegram.error.Forbidden:
            logger.info(f"FORBIDDEN: Message couldn't be delivered to {user['user_id']}")
            continue
        except telegram.error.BadRequest:
            logger.info(f"BAD REQUEST: Message couldn't be delivered to {user['user_id']}")
            continue
        except telegram.error.TimedOut:
            # Message might be still sent to the user even if Telegram doesn't return a response
            # That's why I'm not trying to resend the message. If this is not the case FIXME.
            logger.info(f"WARNING: Telegram didn't return a response in time while sending a message to "
                        f"{user['user_id']}")
            continue


# UTILS
def compare(olds: list[dict], news: list[dict]) -> list[dict]:
    """
    Compares between two announcement lists, returns new ones.
    :param olds: Old announcements
    :param news: Possible new announcements
    :return: Different announcements
    """

    diff = []
    for announcement in news:
        if announcement not in olds:
            diff.append(announcement)
    return diff


def create_announcement_message(department_id: str, announcement: dict, language: str) -> str:
    """
    Creates an announcement message to send.
    :param department_id: The department's id that has the new announcement
    :param announcement: The announcement that will be shared
    :param language: Language that the message will be displayed
    :return: Announcement message
    """

    title = announcement['title']
    content = announcement['content']
    url = announcement['url']
    message = f"<b>{decode(department_id, language)} {decode('announcement-header', language)}</b>\n\n\n"

    for key in announcement.keys():
        if key == 'title' and title is not None:
            message += f"\U0001F514 <b>{title}</b>\n\n"

        if key == 'content' and content is not None:
            message += f"\U0001F4AC {content}\n\n"

        if key == 'url' and url is not None:
            message += f"\U0001F310 <a href='{url}'>{decode('details-anchor-text', language)}</a>"

    return message
