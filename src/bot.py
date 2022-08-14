import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

import Task
import config
from src.handler import CallbackQueryHandler as Cqh, CommandHandler as Ch, MessageHandler as Mh


def main():
    TOKEN = config.API_KEY
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('feedback', Ch.feedback)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, Mh.feedback_done)]
        },
        fallbacks=[CommandHandler('cancel', Ch.cancel)]
    ))

    dispatcher.add_handler(CommandHandler('start', Ch.start))
    dispatcher.add_handler(CommandHandler('help', Ch.help))
    dispatcher.add_handler(CommandHandler('add', Ch.new_subscription))
    dispatcher.add_handler(CommandHandler('remove', Ch.remove_subscription))
    dispatcher.add_handler(CommandHandler('reset', Ch.reset_subscriptions))
    dispatcher.add_handler(CommandHandler('settings', Ch.settings))
    dispatcher.add_handler(CommandHandler('donate', Ch.donate))
    dispatcher.add_handler(CommandHandler('answer', Ch.answer_feedback))
    dispatcher.add_handler(CommandHandler('new_department', Ch.add_new_department))
    dispatcher.add_handler(CommandHandler('send_from_admin', Ch.send_from_admin))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, Mh.edit_subscription))
    dispatcher.add_handler(CallbackQueryHandler(Cqh.button))

    updater.job_queue.run_repeating(Task.check_announcements, interval=600, first=1)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://hu-announcement-bot.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
