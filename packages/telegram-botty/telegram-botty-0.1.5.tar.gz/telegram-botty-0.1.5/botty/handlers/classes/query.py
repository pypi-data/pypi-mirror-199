from abc import ABC

from telegram import ext

from botty.errors import CallbackDataError
from botty.handlers.types import PTBHandler
from botty.helpers import listify
from botty.types import Query

from .update import UpdateHandler


class QueryHandler(UpdateHandler, ABC):
    on_button: str | list[str]

    @classmethod
    def build(cls) -> PTBHandler:
        return ext.CallbackQueryHandler(cls._handle, cls._filter)

    @classmethod
    def _filter(cls, callback_data: object) -> bool:
        if not isinstance(callback_data, str):
            raise CallbackDataError(callback_data)
        cls._validate_class_field("on_button")
        return callback_data in listify(cls.on_button)

    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        raw = self.update.callback_query
        if raw is None:
            self._raise_field_error("query")
        return Query(raw)
