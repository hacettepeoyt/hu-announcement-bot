from . import bot
from . import config


def validate():
    if not config.TELEGRAM_API_KEY:
        print("ERROR: Please configure TELEGRAM API KEY")
        exit(2)

    if not config.DB_STRING:
        print("ERROR: Please configure DB_STRING")
        exit(2)

    if not config.DB_NAME:
        print("ERROR: Please configure DB_NAME")
        exit(2)

    if config.ADMIN_ID == 0:
        print("ERROR: Please configure ADMIN_ID")
        exit(2)

    if config.FEEDBACK_CHAT_ID == config.ADMIN_ID:
        print("WARNING: FEEDBACK_CHAT_ID and ADMIN_ID are same")

    if config.LOGGER_CHAT_ID == config.ADMIN_ID:
        print("WARNING: LOGGER_CHAT_ID and ADMIN_ID are same")

    if config.ANNOUNCEMENT_CHECK_INTERVAL <= 0:
        print("ERROR: Please configure ANNOUNCEMENT_CHECK_INTERVAL greater than 0")
        exit(2)

    if config.WEBHOOK_CONNECTED:
        if config.WEBHOOK_URL[1:] == config.TELEGRAM_API_KEY:
            print("ERROR: Please make sure you configured a WEBHOOK_URL when WEBHOOK_CONNECTED is True")
            exit(2)

        if not config.PORT:
            print("ERROR: Please make sure you configured a valid PORT number when WEBHOOK_CONNECTED is True")
            exit(2)


if __name__ == '__main__':
    validate()
    bot.main()
