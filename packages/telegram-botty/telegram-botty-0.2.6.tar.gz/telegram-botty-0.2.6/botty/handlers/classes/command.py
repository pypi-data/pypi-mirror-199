from abc import ABC

from telegram import ext

from botty.types import PTBHandler

from .text import TextHandler


class CommandHandler(TextHandler, ABC):
    def __init__(self, command: str) -> None:
        self.on_command = command
        super().__init__()

    def build(self) -> PTBHandler:
        return ext.CommandHandler(self.on_command, self.handle, self.filters)
