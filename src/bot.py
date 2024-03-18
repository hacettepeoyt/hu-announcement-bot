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

    # In python-telegram-bot, handlers have something called group. It means that whenever there is
    # a new update from Telegram, this update runs through each of these groups. This update can be
    # handled by a handler from group 2, and it can be handled by another handler from group 7 at
    # the same time. Handling updates sounds like we have only one chance to do something at first,
    # but no. We can handle it however we like. Handlers are completely seperated and don't have any
    # relationship with Telegram. At least I had this misconception for a long time.
    #
    # So, I use grouping to switch context to another conversation, because otherwise updates stuck
    # inside the conversation. Alright then everything seems fine right? Nah...
    #
    # Conversation handling is a bit tricky, especially when it comes to nested conversations.
    # I want to have a really simple conversation flow with the users. It should be like following:
    # When the user starts a new conversation, let's call it conv_1, conversation should start
    # normally. Then, when she decides to start another conversation, let's say conv_2, it should
    # end the conv_1 and continue normally within the conv_2. There mustn't be a nested conversation!
    # Therefore, we need to kill the previous conversations. There isn't an obvious way to kill a
    # conversation unless you want to manually use _update_state() method. Here comes my tricky
    # solution. I put a MessageHandler into fallback that filters only commands. Fallback means if the
    # update can't be handled inside the states, it goes to fallbacks and see if it can find a proper
    # handler there. When user starts conv_2, she has to use a specific command let's say /start_conv_2.
    # conv_1_handler won't find a proper handler for /start_conv_2, so it will fall, then our tricky
    # MessageHandler will catch it. It will kill the current conversation. Then the update will travel
    # through other groups. This way we will have only one alive conversation. This tricky MessageHandler
    # is given below.
    conversation_switch_handler = MessageHandler(filters.COMMAND, handler.cancel)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('feedback', handler.feedback)],
        states={
            1: [MessageHandler(~filters.COMMAND, handler.feedback_done)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[
            CommandHandler('done', handler.done),
            conversation_switch_handler
        ],
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
        fallbacks=[
            CommandHandler('done', handler.done),
            conversation_switch_handler
        ],
        allow_reentry=True,
        conversation_timeout=ADMIN_ANNOUNCEMENT_TIMEOUT
    ), group=3)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', handler.add)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.add_subscription)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[
            CommandHandler('done', handler.done),
            conversation_switch_handler
        ],
        allow_reentry=True,
        conversation_timeout=ADD_TIMEOUT
    ), group=4)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('remove', handler.remove)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.remove_subscription)],
            ConversationHandler.TIMEOUT: [TypeHandler(Update, handler.conversation_timeout)]
        },
        fallbacks=[
            CommandHandler('done', handler.done),
            conversation_switch_handler
        ],
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
