from abc import ABC

from telegram import ext

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    def __init__(self, reply_text: str | None = None) -> None:
        super().__init__("start", reply_text)


class StartGroupHandler(StartHandler):
    filters = StartHandler.filters & ext.filters.ChatType.GROUPS
