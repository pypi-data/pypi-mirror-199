from abc import ABC

from telegram import ext

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    def __init__(self) -> None:
        super().__init__("start")


class StartGroupHandler(StartHandler):
    filters = StartHandler.filters & ext.filters.ChatType.GROUPS
