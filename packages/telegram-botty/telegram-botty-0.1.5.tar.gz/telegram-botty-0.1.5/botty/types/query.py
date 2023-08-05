import telegram

from botty.errors import FieldError


class Query:
    def __init__(self, raw: telegram.CallbackQuery) -> None:
        self.raw = raw

    @property
    def data(self) -> str:
        value = self.raw.data
        if value is None:
            raise FieldError(self.raw, "data")
        return value

    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.raw.answer(text, show_alert)
