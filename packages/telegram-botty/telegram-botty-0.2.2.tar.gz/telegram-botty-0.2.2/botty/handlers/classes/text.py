from abc import ABC

from telegram import ext

from botty.types import PTBHandler

from .message import MessageHandler


class TextHandler(MessageHandler, ABC):
    filters = MessageHandler.filters & ext.filters.TEXT

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)
