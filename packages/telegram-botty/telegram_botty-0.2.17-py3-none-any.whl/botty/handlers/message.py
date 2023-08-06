import telegram
from botty_core.types import Chat, Message, PTBHandler, ReplyMarkup, User
from telegram import ext

from botty.keyboards import InlineKeyboard

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def __init__(
        self,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        self.reply_text = reply_text
        self.reply_keyboard = reply_keyboard
        super().__init__()

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)

    async def callback(self) -> None:
        text = self.get_reply_text()
        if text:
            markup = self.get_reply_markup()
            await self.reply(text, markup)

    def get_reply_text(self) -> str | None:
        return self.reply_text

    def get_reply_markup(self) -> ReplyMarkup | None:
        keyboard = self.get_reply_keyboard()
        return None if keyboard is None else keyboard.build()

    def get_reply_keyboard(self) -> InlineKeyboard | None:
        return self.reply_keyboard

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
