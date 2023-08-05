from abc import ABC

from telegram import ext

from botty.handlers.types import PTBHandler

from .text import TextHandler


class CommandHandler(TextHandler, ABC):
    on_command: str

    @classmethod
    def build(cls) -> PTBHandler:
        cls._validate_class_field("on_command")
        return ext.CommandHandler(cls.on_command, cls._handle, cls.filters)
