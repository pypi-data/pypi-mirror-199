from abc import ABC

from botty_core.types import PTBHandler, Query
from telegram import ext

from botty.buttons import CallbackButton
from botty.errors import CallbackDataError

from .update import UpdateHandler


class QueryHandler(UpdateHandler, ABC):
    def __init__(self, button: CallbackButton | None = None) -> None:
        callback_data = None if button is None else button.callback_data
        validate_callback_data(callback_data)
        self.on_callback_data = callback_data
        super().__init__()

    def build(self) -> PTBHandler:
        return ext.CallbackQueryHandler(self.handle, self._filter)

    def _filter(self, callback_data: object) -> bool:
        validate_callback_data(callback_data)
        if self.on_callback_data is None:
            return True
        return callback_data == self.on_callback_data

    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        return self.update.query


def validate_callback_data(callback_data: object) -> None:
    if not isinstance(callback_data, str):
        raise CallbackDataError(callback_data)
