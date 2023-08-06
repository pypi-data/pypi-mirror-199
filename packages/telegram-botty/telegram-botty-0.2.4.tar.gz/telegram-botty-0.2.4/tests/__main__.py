from botty import CommandHandler, CompositeHandler, StartHandler, app


class HelloHandler(StartHandler):
    async def callback(self) -> None:
        await self.reply("Hello")


class HelpHandler(CommandHandler):
    async def callback(self) -> None:
        await self.reply("Help")


handler = CompositeHandler(HelloHandler(), HelpHandler("help"))
app.run(handler)
