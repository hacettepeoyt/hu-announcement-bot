from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, \
    filters, TypeHandler

from . import handler, task
from .config import TELEGRAM_API_KEY, ANNOUNCEMENT_CHECK_INTERVAL, ANNOUNCEMENT_CHECK_FIRST, WEBHOOK_CONNECTED, PORT, \
    WEBHOOK_URL, FEEDBACK_TIMEOUT, ADMIN_ANNOUNCEMENT_TIMEOUT, ADD_TIMEOUT, REMOVE_TIMEOUT


def main() -> None:
    app: Application = Application.builder().token(TELEGRAM_API_KEY).build()

    app.add_handler(CommandHandler('start', handler.start), group=1)
    app.add_handler(CommandHandler('help', handler.help), group=1)
    app.add_handler(CommandHandler('reset', handler.reset_subscriptions), group=1)
    app.add_handler(CommandHandler('settings', handler.settings), group=1)
    app.add_handler(CommandHandler('donate', handler.donate), group=1)
    app.add_handler(CommandHandler('answer', handler.answer), group=1)
    app.add_handler(CommandHandler('activate_department', handler.activate_department), group=1)
    app.add_handler(CommandHandler('deactivate_department', handler.deactivate_department), group=1)
    app.add_handler(CallbackQueryHandler(handler.settings_buttons), group=1)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('feedback', handler.feedback)],
        states={
            1: [MessageHandler(~filters.COMMAND, handler.feedback_done)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True,
        conversation_timeout=FEEDBACK_TIMEOUT
    ), group=2)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('admin_announcement', handler.admin_announcement)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.admin_announcement_choose_department)],
            2: [MessageHandler(~filters.COMMAND, handler.admin_announcement_done)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True,
        conversation_timeout=ADMIN_ANNOUNCEMENT_TIMEOUT
    ), group=3)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', handler.add)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.add_subscription)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True,
        conversation_timeout=ADD_TIMEOUT
    ), group=4)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('remove', handler.remove)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.remove_subscription)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True,
        conversation_timeout=REMOVE_TIMEOUT
    ), group=5)

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
