from . import bot
from . import config


def validate():
    if not config.TELEGRAM_API_KEY:
        print("ERROR: Please configure TELEGRAM API KEY")
        exit(-1)

    if not config.DB_STRING:
        print("ERROR: Please configure DB_STRING")
        exit(-1)

    if config.ADMIN_ID == 0:
        print("WARNING: You didn't configured an ADMIN_ID, so you won't be able to use admin commands!")

    if config.FEEDBACK_CHAT_ID == 0:
        print("ERROR: Please configure FEEDBACK_CHAT_ID")
        exit(-1)

    if config.LOGGER_CHAT_ID == 0:
        print("ERROR: Please configure LOGGER_CHAT_ID")
        exit(-1)

    if config.ANNOUNCEMENT_CHECK_INTERVAL == 0:
        print("ERROR: Please configure ANNOUNCEMENT_CHECK_INTERVAL")
        exit(-1)

    if config.WEBHOOK_CONNECTED:
        if config.WEBHOOK_URL == config.TELEGRAM_API_KEY:
            print("ERROR: Please make sure you configured a WEBHOOK_URL if you are using webhook rather than polling!")

        if not config.PORT:
            print("ERROR: Please make sure you configured a valid PORT number!")

        exit(-1)


if __name__ == '__main__':
    validate()
    bot.main()
