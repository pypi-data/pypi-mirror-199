from abc import ABC

from telegram import ext

from botty.errors import CallbackDataError
from botty.helpers import listify
from botty.types import PTBHandler, Query

from .update import UpdateHandler


class QueryHandler(UpdateHandler, ABC):
    def __init__(self, button: str | list[str]) -> None:
        self.on_button = button
        super().__init__()

    def build(self) -> PTBHandler:
        return ext.CallbackQueryHandler(self.handle, self._filter)

    def _filter(self, callback_data: object) -> bool:
        if not isinstance(callback_data, str):
            raise CallbackDataError(callback_data)
        return callback_data in listify(self.on_button)

    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        return self.update.query
