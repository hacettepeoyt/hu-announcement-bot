from typing import Optional

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from ..mongo import user_db
from ..abc import Backend, Messageable, User
from ..cmd import Context
from ..handler import cb_query_handler as Cqh, cmd_handler as Ch, msg_handler as Mh
from ..scraper.index import availableDepartments


class TelegramChat(Messageable):
    _bot: telegram.Bot
    _id: int

    def __init__(self, _id: int, bot: telegram.Bot):
        self._id = _id
        self._bot = bot

    def send(self, content: str, *args, **kwargs):
        self._bot.send_message(chat_id=self._id, text=content, **kwargs)


class TelegramUser(TelegramChat, User):
    dnd: bool
    language: str
    holiday_mode: bool
    subscriptions: list[str]

    def __init__(self, _id: int, bot: telegram.Bot, first_name: Optional[str] = None, last_name: Optional[str] = None,
                 language: Optional[str] = None):
        super().__init__(_id, bot)
        props = user_db.get_properties(_id, ('first_name', 'last_name', 'dnd', 'holiday_mode', 'language'))
        self.first_name = first_name or props['first_name']
        self.last_name = last_name or props['last_name']
        self.dnd = props['dnd'] or False
        self.language = language or props['language']
        self.holiday_mode = props['holiday_mode'] or False
        self.subscriptions = user_db.find_subscriptions(_id) or ['hu-3', 'hu-13']

    def __eq__(self, other: object):
        if not isinstance(other, TelegramUser):
            return False

        return self._id == other._id

    def get_dnd(self) -> bool:
        return self.dnd

    def set_dnd(self, dnd: bool):
        user_db.set_customs(self._id, 'dnd', dnd)
        self.dnd = dnd

    def get_language(self) -> str:
        return self.language

    def set_language(self, language: str):
        user_db.set_customs(self._id, 'language', language)
        self.language = language

    def get_holiday_mode(self) -> bool:
        return self.holiday_mode

    def set_holiday_mode(self, mode: bool) -> None:
        user_db.set_customs(self._id, 'holiday_mode', mode)
        self.holiday_mode = mode

    def get_subscriptions(self) -> list[str]:
        return self.subscriptions

    def set_subscriptions(self, departments: list[str]) -> None:
        if __debug__:
            for department in departments:
                assert department in availableDepartments
        user_db.update_subscriptions(self._id, departments)
        self.departments = departments

    def add_subscription(self, department: str) -> bool:
        if department not in availableDepartments:
            return False

        subs = self.get_subscriptions()
        subs.append(department)
        self.set_subscriptions(subs)
        return True

    def remove_subscription(self, department: str) -> bool:
        subs = self.get_subscriptions()

        try:
            subs.remove(department)
        except ValueError:
            return False

        self.set_subscriptions(subs)
        return True


class TelegramBackend(Backend):
    _updater: Updater
    token: str
    users: dict[int, TelegramUser]

    def __init__(self, bot, token: str, webhook_url: str, admin_id: int):
        self._bot = bot
        self._token = token
        self._admin_id = admin_id
        self.users = {}
        self.webhook_url = webhook_url

        self._updater = Updater(token)
        dispatcher = self._updater.dispatcher

        dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('feedback', Ch.feedback)],
            states={
                1: [MessageHandler(Filters.text & ~Filters.command, Mh.feedback_done)]
            },
            fallbacks=[CommandHandler('cancel', Ch.cancel)]
        ))

        dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, self._handle_message))

    def _user_from_module(self, effective_user) -> TelegramUser:
        """ Returns an user from the backend cache or create a new one from a python-telegram-bot User. """
        if effective_user.id in self.users:
            return self.users[effective_user.id]

        user = TelegramUser(_id=effective_user.id, bot=self._updater.bot,
                            first_name=effective_user.first_name, last_name=effective_user.last_name,
                            language=effective_user.language_code)
        self.users[effective_user.id] = user

        return user

    def _handle_message(self, update, _) -> None:
        ctx = Context(bot=self._bot,
                      backend='telegram',
                      author=self._user_from_module(update.effective_user),
                      channel=TelegramChat(_id=update.message.chat.id, bot=self._updater.bot),
                      message=update.message.text)
        self._bot.on_message(ctx, update.message.text)

    def get_admin(self) -> TelegramUser:
        return self.get_user(self._admin_id)

    def get_user(self, id: int) -> TelegramUser:
        if id in self.users:
            return self.users[id]

        user = self.users[id] = TelegramUser(_id=id, bot=self._updater.bot)
        return user

    def get_me(self) -> TelegramUser:
        return self._user_from_module(self._updater.bot.bot)

    def run(self):
        if self.webhook_url:
            self._updater.start_webhook(listen="0.0.0.0",
                                        port=8443,  #TODO: de-hardcode this.
                                        url_path=self._token,
                                        webhook_url=self.webhook_url)
        else:
            self._updater.start_polling()
