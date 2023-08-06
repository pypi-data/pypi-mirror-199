import telegram
from botty_core.types import Chat, Message, PTBHandler, ReplyMarkup, User
from telegram import ext

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE
    reply_markup: ReplyMarkup | None = None

    def __init__(self, reply_text: str | None = None) -> None:
        self.reply_text = reply_text
        super().__init__()

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)

    async def callback(self) -> None:
        text = self.get_reply_text()
        markup = self.get_reply_markup()
        await self.reply(text, markup)

    def get_reply_text(self) -> str:
        return self.get_validated_field("reply_text", self.reply_text)

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        return await self.message.reply(text, markup)

    @property
    def message(self) -> Message:
        return self.update.message

    @property
    def chat(self) -> Chat:
        return self.message.chat

    @property
    def user(self) -> User:
        return self.message.user

    @property
    def text(self) -> str:
        return self.message.text
