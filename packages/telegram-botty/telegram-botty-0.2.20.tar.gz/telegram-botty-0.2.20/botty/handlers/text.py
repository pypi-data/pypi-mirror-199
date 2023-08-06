from abc import ABC

from botty_core.types import PTBHandler
from telegram import ext

from .message import MessageHandler


class TextHandler(MessageHandler, ABC):
    filters = MessageHandler.filters & ext.filters.TEXT

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)

    @property
    def text(self) -> str:
        return self.message.text

    @property
    def text_words(self) -> list[str]:
        return self.text.lower().split()
