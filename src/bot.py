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
from typing import Callable

import config
from . import abc, cmd, task
from .backend.telegram import TelegramBackend
from .handler import cmd_handler


BACKENDS: dict[str, type] = {'telegram': TelegramBackend}


class Bot:
    backends: dict[str, abc.Backend]
    cmd_handler: cmd.CommandParser
    event_hooks: dict[str, list[Callable[[cmd.Context], bool]]]

    def __init__(self, *args, **kwargs):
        self.backends = {}
        for name, backend in BACKENDS.items():
            self.backends[name] = backend(bot=self, **kwargs.get(f"{name}_options", {}))
        self.users = []
        self.cmd_handler = cmd.CommandParser(cmd.on_prefix("/"))
        self.event_hooks = {'message': []}
        self.command = self.cmd_handler.command

    def run(self):
        for backend in self.backends.values():
            backend.run()

        while True:
            task.check_announcements(self)
            time.sleep(600)

    def get_user(self, backend: str, user_id: int) -> abc.User:
        return self.backends[backend].get_user(user_id)

    def hook(self, event_type: str, hook: Callable[[cmd.Context], bool]) -> None:
        self.event_hooks[event_type].append(hook)

    def on_message(self, ctx: cmd.Context, message: str) -> None:
        # Do not trigger on_message if the message was sent from the bot.
        if ctx.author == self.backends[ctx.backend].get_me():
            return
 
        triggered_hooks: list[Callable[[cmd.Context], bool]] = []
        for hook in self.event_hooks['message']:
            if hook(ctx):
                triggered_hooks.append(hook)

        if triggered_hooks:
            for hook in triggered_hooks:
                self.event_hooks['message'].remove(hook)
        else:
            # Do not trigger the command handler if a hook was triggered.
            self.cmd_handler.parse_command(ctx, message)


def main():
    bot = Bot(telegram_options={"token": config.API_KEY, "webhook_url": config.WEBHOOK_URL, 'admin_id': config.ADMIN_ID})

    # TODO: Reorganize the code to properly use this as decorators?
    bot.command()(cmd_handler.start)
    bot.command()(cmd_handler.help)
    bot.command("add")(cmd_handler.new_subscription)
    bot.command("remove")(cmd_handler.remove_subscription)
    bot.command("reset")(cmd_handler.reset_subscriptions)
    bot.command()(cmd_handler.settings)
    bot.command()(cmd_handler.donate)
    bot.command()(cmd_handler.feedback)
    bot.command()(cmd_handler.answer_feedback)
    bot.command()(cmd_handler.add_new_department)
    bot.command()(cmd_handler.send_from_admin)

    bot.run()


if __name__ == '__main__':
    main()
    
