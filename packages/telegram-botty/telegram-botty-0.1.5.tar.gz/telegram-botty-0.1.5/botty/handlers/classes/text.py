from abc import ABC

from telegram import ext

from botty.handlers.types import PTBHandler

from .message import MessageHandler


class TextHandler(MessageHandler, ABC):
    filters = MessageHandler.filters & ext.filters.TEXT

    @classmethod
    def build(cls) -> PTBHandler:
        return ext.MessageHandler(cls.filters, cls._handle)
