from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters

from . import handler, task
from .config import TELEGRAM_API_KEY, ANNOUNCEMENT_CHECK_INTERVAL, ANNOUNCEMENT_CHECK_FIRST, WEBHOOK_CONNECTED, PORT, \
    WEBHOOK_URL


def main() -> None:
    app: Application = Application.builder().token(TELEGRAM_API_KEY).build()

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('feedback', handler.feedback)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.feedback_done)]
        },
        fallbacks=[CommandHandler('cancel', handler.cancel)]
    ))

    app.add_handler(CommandHandler('start', handler.start))
    app.add_handler(CommandHandler('help', handler.help))
    app.add_handler(CommandHandler('add', handler.new_subscription))
    app.add_handler(CommandHandler('remove', handler.remove_subscription))
    app.add_handler(CommandHandler('reset', handler.reset_subscriptions))
    app.add_handler(CommandHandler('settings', handler.settings))
    app.add_handler(CommandHandler('donate', handler.donate))
    app.add_handler(CommandHandler('admin_announcement', handler.admin_announcement))
    app.add_handler(CommandHandler('answer', handler.answer))
    app.add_handler(CallbackQueryHandler(handler.settings_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.update_subscription))
    app.add_error_handler(handler.err_handler)
    app.job_queue.run_repeating(task.check_announcements, interval=ANNOUNCEMENT_CHECK_INTERVAL,
                                first=ANNOUNCEMENT_CHECK_FIRST)

    if WEBHOOK_CONNECTED:
        app.run_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TELEGRAM_API_KEY,
                        webhook_url=WEBHOOK_URL)
    else:
        app.run_polling()


if __name__ == "__main__":
    main()
