import telegram

from botty.telegram_object import TelegramObject


class Query(TelegramObject):
    raw: telegram.CallbackQuery

    def __init__(self, raw: telegram.CallbackQuery) -> None:
        super().__init__(raw)

    @property
    def data(self) -> str:
        return self.get_validated_field("data", self.raw.data)

    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.raw.answer(text, show_alert)
