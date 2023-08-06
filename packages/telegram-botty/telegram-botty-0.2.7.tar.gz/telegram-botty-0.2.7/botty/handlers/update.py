from abc import ABC, abstractmethod
from copy import deepcopy

import telegram
from botty_core import Handler
from botty_core.types import Bot, Context, PTBHandler, Update
from telegram import ext


class UpdateHandler(Handler, ABC):
    def __init__(self) -> None:
        self._update: Update | None = None
        self._context: Context | None = None

    def build(self) -> PTBHandler:
        return ext.TypeHandler(telegram.Update, self.handle)

    async def handle(self, update: telegram.Update, context: Context) -> None:
        handler = deepcopy(self)
        handler.set_update(update, context)
        await handler.prepare()
        await handler.callback()

    def set_update(self, update: telegram.Update, context: Context) -> None:
        self._update = Update(update)
        self._context = context

    @abstractmethod
    async def callback(self) -> None:
        """Will be called to handle update."""

    async def prepare(self) -> None:
        """Will be called before `callback`."""

    @property
    def update(self) -> Update:
        return self.get_validated_field("update", self._update)

    @property
    def context(self) -> Context:
        return self.get_validated_field("context", self._context)

    @property
    def bot(self) -> Bot:
        raw = self.context.bot
        return Bot(raw)
