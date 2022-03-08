import telegram
import config
import logging
import scraper

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

math_website = scraper.Math()
sksdb_website = scraper.Sksdb()

websites = [sksdb_website, math_website]


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_name = user['first_name']
    print(user['id'])

    update.message.reply_text(f"Hi {user_name}! I'm not fully live yet, coming soon!")


def isOnline(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user['id']

    context.bot.send_message(chat_id=user_id, text="*Yes, I'm still alive*\n"
                                                   "[Click here](www.cs.hacettepe.edu.tr)\.",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2,
                             disable_web_page_preview=True)


def check_newAnnouncements(context: CallbackContext):
    for website in websites:
        announcement = website.get_announcement()

        if announcement is not None:
            title = announcement['title']
            content = announcement['content']
            url = announcement['url']

            context.bot.send_message(chat_id=config.admin_id, text=f"\U0001F514 <b>{title}</b>\n\n"
                                                                   f"\U0001F4AC {content}\n\n"
                                                                   f'\U0001F310 <a href="{url}">Click here!</a>',
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)


def main():
    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CommandHandler("online_status", isOnline))

    updater.job_queue.run_repeating(check_newAnnouncements, interval=20, first=1)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
