from botty import CommandHandler, Handlers, StartHandler, app


class HelloHandler(StartHandler):
    async def callback(self) -> None:
        await self.reply("Hello")


class HelpHandler(CommandHandler):
    async def callback(self) -> None:
        await self.reply("Help")


HANDLERS = Handlers(HelloHandler(), HelpHandler("help"))
app.run(HANDLERS)
