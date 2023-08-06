from botty import CommandHandler, CompositeHandler, StartHandler, app

handler = CompositeHandler(
    StartHandler("Hello"),
    CommandHandler("help", "Help"),
)

app.run(handler)
