from abc import ABC, abstractmethod
from typing import NoReturn

from telegram import Update, ext

from botty.errors import FieldError
from botty.handlers.handler import Handler
from botty.handlers.types import Context, PTBHandler
from botty.types import Bot


class UpdateHandler(Handler, ABC):
    def __init__(self, update: Update, context: Context) -> None:
        self.update = update
        self.context = context

    @classmethod
    def build(cls) -> PTBHandler:
        return ext.TypeHandler(Update, cls._handle)

    @classmethod
    async def _handle(cls, update: Update, context: Context) -> None:
        handler = cls(update, context)
        await handler.prepare()
        await handler.callback()

    @abstractmethod
    async def callback(self) -> None:
        """Will be called to handle update."""

    async def prepare(self) -> None:
        """Will be called before `callback`."""

    @property
    def bot(self) -> Bot:
        raw = self.context.bot
        return Bot(raw)

    def _raise_field_error(self, field: str) -> NoReturn:
        raise FieldError(self.update, field)
