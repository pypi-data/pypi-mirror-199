import telegram
from telegram import ext

from botty.types import Chat, Message, PTBHandler, ReplyMarkup, User

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE
    reply_text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)

    async def callback(self) -> None:
        text = self.get_validated_field("reply_text", self.reply_text)
        await self.reply(text, self.reply_markup)

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
