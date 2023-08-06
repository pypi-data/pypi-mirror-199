from abc import ABC

from telegram import ext

from botty.keyboards import InlineKeyboard

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    def __init__(
        self,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__("start", reply_text, reply_keyboard)


class StartGroupHandler(StartHandler):
    filters = StartHandler.filters & ext.filters.ChatType.GROUPS
