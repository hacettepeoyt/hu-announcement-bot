'''
        This module is the core of the Telegram API for this project.
        There are plenty of requests can be made by the users. For example,
        sending commands, messages, photos, location... clicking inline buttons,
        normal buttons etc. Telegram API provides really good variety of requests.

        This module get some of those requests and route them to handler modules
        that in src/handler

        Hacettepe Duyurucusu uses webhook rather than polling, because it's more
        efficient and since it lives on Heroku, it'd be more reasonable to tell
        Telegram where it lives and get requests there.

        Bot has one job to do regulary. It's the checking for new announcements.
        python-telegram-api provides a scheduler, I used that.
'''


import time

import Task
import config
from src import _abc
from src.backend.telegram import TelegramBackend


BACKENDS: dict[str, type] = {'telegram': TelegramBackend}


class Bot:
    backends: dict[str, _abc.Backend]

    def __init__(self, *args, **kwargs):
        self.backends = {}
        for name, backend in BACKENDS.items():
            self.backends[name] = backend(bot=self, **kwargs.get(f"{name}_options", {}))
        self.users = []

    def run(self):
        for backend in self.backends.values():
            backend.run()

        while True:
            Task.check_announcements(self)
            time.sleep(600)

    def get_user(self, backend: str, user_id: int) -> _abc.User:
        return self.backends[backend].get_user(user_id)


def main():
    bot = Bot(telegram_options={"token": config.API_KEY, "webhook_url": config.WEBHOOK_URL})
    bot.run()


if __name__ == '__main__':
    main()
    
