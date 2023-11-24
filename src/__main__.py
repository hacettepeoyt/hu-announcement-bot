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
        print("WARNING: You didn't configured an ADMIN_ID, so you won't be able to use admin commands!")

    if config.FEEDBACK_CHAT_ID == 0:
        print("ERROR: Please configure FEEDBACK_CHAT_ID")
        exit(2)

    if config.LOGGER_CHAT_ID == 0:
        print("ERROR: Please configure LOGGER_CHAT_ID")
        exit(2)

    if config.ANNOUNCEMENT_CHECK_INTERVAL == 0:
        print("ERROR: Please configure ANNOUNCEMENT_CHECK_INTERVAL")
        exit(2)

    if config.WEBHOOK_CONNECTED:
        if config.WEBHOOK_URL == config.TELEGRAM_API_KEY:
            print("ERROR: Please make sure you configured a WEBHOOK_URL if you are using webhook rather than polling!")
            exit(2)

        if not config.PORT:
            print("ERROR: Please make sure you configured a valid PORT number!")
            exit(2)


if __name__ == '__main__':
    validate()
    bot.main()
