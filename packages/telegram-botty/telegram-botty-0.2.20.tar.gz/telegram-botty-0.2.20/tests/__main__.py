from botty import CommandHandler, CompositeHandler, QueryHandler, StartHandler, app


class TestHandler(CommandHandler):
    def __init__(self) -> None:
        super().__init__("test")

    async def callback(self) -> None:
        await self.reply(str(self.get_reply_text()))
        await super().callback()


handler = CompositeHandler(
    StartHandler("Hello"),
    CommandHandler("help", "Help"),
    TestHandler(),
    QueryHandler(reply_text="?"),
)

app.run(handler)
