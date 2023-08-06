from abc import ABC

from botty_core.types import PTBHandler
from telegram import ext

from .text import TextHandler


class CommandHandler(TextHandler, ABC):
    def __init__(self, command: str, reply_text: str | None = None) -> None:
        self.on_command = command
        super().__init__(reply_text)

    def build(self) -> PTBHandler:
        return ext.CommandHandler(self.on_command, self.handle, self.filters)
