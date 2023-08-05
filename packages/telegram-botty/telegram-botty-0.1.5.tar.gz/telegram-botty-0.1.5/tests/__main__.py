from botty import CommandHandler, Handlers, StartHandler, app


class HelloHandler(StartHandler):
    async def callback(self) -> None:
        await self.reply("Hello")


class HelpHandler(CommandHandler):
    on_command = "help"

    async def callback(self) -> None:
        await self.reply("Help")


HANDLERS = Handlers(HelloHandler, HelpHandler)
app.run(HANDLERS)
