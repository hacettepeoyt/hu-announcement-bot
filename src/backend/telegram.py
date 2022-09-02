import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from ..mongo import user_db
from ..abc import Backend, User
from ..handler import cb_query_handler as Cqh, cmd_handler as Ch, msg_handler as Mh


class TelegramUser(User):
    _bot: telegram.Bot
    _id: int
    dnd: bool
    language: str

    def __init__(self, _id: int, bot: telegram.Bot):
        self._id = _id
        self._bot = bot
        self.dnd = user_db.get_property(self._id, 'dnd')
        self.language = user_db.get_property(self._id, 'language')

    def send(self, content: str, **kwargs):
        self._bot.send_message(chat_id=self._id, text=content, **kwargs)

    def get_dnd(self) -> bool:
        return self.dnd

    def set_dnd(self, dnd: bool):
        user_db.set_customs(self._id, 'dnd', dnd)
        self.dnd = dnd

    def get_language(self) -> str:
        return self.language

    def set_language(self, language: str):
        user_db.set_customs(self._id, 'dnd', language)
        self.language = language


class TelegramBackend(Backend):
    _updater: Updater
    token: str
    users: dict[int, TelegramUser]

    def __init__(self, bot, token: str, webhook_url: str):
        self._bot = bot
        self._token = token
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

        # TODO: Do not use Telegram backend's CommandHandlers.
        dispatcher.add_handler(CommandHandler('start', Ch.start))
        dispatcher.add_handler(CommandHandler('help', Ch.help))
        dispatcher.add_handler(CommandHandler('add', Ch.new_subscription))
        dispatcher.add_handler(CommandHandler('remove', Ch.remove_subscription))
        dispatcher.add_handler(CommandHandler('reset', Ch.reset_subscriptions))
        dispatcher.add_handler(CommandHandler('settings', Ch.settings))
        dispatcher.add_handler(CommandHandler('donate', Ch.donate))
        dispatcher.add_handler(CommandHandler('answer', Ch.answer_feedback))
        dispatcher.add_handler(CommandHandler('new_department', Ch.add_new_department))
        dispatcher.add_handler(CommandHandler('send_from_admin', Ch.send_from_admin))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, Mh.edit_subscription))
        dispatcher.add_handler(CallbackQueryHandler(Cqh.main))

    def get_user(self, id: int) -> TelegramUser:
        user = self.users[id] = self.users.get(id, TelegramUser(_id=id, bot=self._updater.bot))

        return user

    def run(self):
        if self.webhook_url:
            self._updater.start_webhook(listen="0.0.0.0",
                                        port=8443,  #TODO: de-hardcode this.
                                        url_path=self._token,
                                        webhook_url=self.webhook_url)
        else:
            self._updater.start_polling()
