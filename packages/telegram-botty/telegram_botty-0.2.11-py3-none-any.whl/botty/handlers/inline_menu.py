from botty.buttons import CallbackButton

from .query import QueryHandler


class InlineMenuHandler(QueryHandler):
    def __init__(self, buttons: dict[CallbackButton, QueryHandler]) -> None:
        self.buttons = buttons
        on_button = [b.text for b in buttons]
        super().__init__(on_button)

    async def callback(self) -> None:
        for button, handler in self.buttons.items():
            if button.callback_data == self.query.data:
                await handler.handle(self.update.raw, self.context)
                break
