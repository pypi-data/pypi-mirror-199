from typing import cast

import telegram
from telegram import ext

from botty.handlers.types import PTBHandler, ReplyMarkup
from botty.types import Chat, User

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE
    reply_text: str
    reply_markup: ReplyMarkup | None = None

    @classmethod
    def build(cls) -> PTBHandler:
        return ext.MessageHandler(cls.filters, cls._handle)

    async def callback(self) -> None:
        self._validate_field("reply_text")
        await self.reply(self.reply_text, self.reply_markup)

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        markup = cast(ReplyMarkup, markup)  # fix PTB error
        return await self.message.reply_text(text, reply_markup=markup)

    @property
    def message(self) -> telegram.Message:
        value = self.update.message
        if value is None:
            self._raise_field_error("message")
        return value

    @property
    def chat(self) -> Chat:
        return Chat(self.message.chat)

    @property
    def user(self) -> User:
        raw = self.message.from_user
        if raw is None:
            self._raise_field_error("user")
        return User(raw)
