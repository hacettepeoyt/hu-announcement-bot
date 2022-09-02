from typing import Optional

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from ..mongo import user_db
from ..abc import Backend, Messageable, User
from ..cmd import Context
from ..handler import cb_query_handler as Cqh, cmd_handler as Ch, msg_handler as Mh


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

    def __init__(self, _id: int, bot: telegram.Bot, first_name: Optional[str] = None, last_name: Optional[str] = None):
        super().__init__(_id, bot)
        props = user_db.get_properties(_id, ('first_name', 'last_name', 'dnd', 'holiday_mode', 'language'))
        self.first_name = first_name or props['first_name']
        self.last_name = last_name or props['last_name']
        self.dnd = props['dnd'] or False
        self.language = props['language']
        self.holiday_mode = props['holiday_mode'] or False

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

        dispatcher.add_handler(MessageHandler(Filters.command, self._handle_command))

    def _user_from_update(self, update) -> TelegramUser:
        """ Returns a user from the cache or from the update. """
        if update.effective_user.id in self.users:
            return self.users[update.effective_user.id]

        user = TelegramUser(_id=update.effective_user.id, bot=self._updater.bot,
                            first_name=update.effective_user.first_name, last_name=update.effective_user.last_name)
        self.users[update.effective_user.id] = user

        return user

    def _handle_command(self, update, _) -> None:
        ctx = Context(bot=self._bot,
                      backend='telegram',
                      author=self.get_user(update.effective_user.id),
                      channel=TelegramChat(_id=update.message.chat.id, bot=self._updater.bot))
        self._bot.cmd_handler.parse_command(ctx, update.message.text)

    def get_admin(self) -> TelegramUser:
        return self.get_user(self._admin_id)

    def get_user(self, id: int) -> TelegramUser:
        if id in self.users:
            return self.users[id]

        user = self.users[id] = TelegramUser(_id=id, bot=self._updater.bot)
        return user

    def run(self):
        if self.webhook_url:
            self._updater.start_webhook(listen="0.0.0.0",
                                        port=8443,  #TODO: de-hardcode this.
                                        url_path=self._token,
                                        webhook_url=self.webhook_url)
        else:
            self._updater.start_polling()
