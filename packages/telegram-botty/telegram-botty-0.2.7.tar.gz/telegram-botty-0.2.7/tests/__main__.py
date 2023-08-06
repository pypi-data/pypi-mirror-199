from botty import CommandHandler, CompositeHandler, StartHandler, app


class HelloHandler(StartHandler):
    reply_text: str = "1"

    async def callback(self) -> None:
        await self.reply(self.reply_text)
        self.reply_text = "2"


class HelpHandler(CommandHandler):
    async def callback(self) -> None:
        await self.reply("Help")


handler = CompositeHandler(HelloHandler(), HelpHandler("help"))
app.run(handler)
