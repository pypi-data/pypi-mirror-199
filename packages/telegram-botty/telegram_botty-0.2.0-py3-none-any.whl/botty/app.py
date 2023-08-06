import warnings

from telegram.constants import ParseMode
from telegram.ext import Application, Defaults
from telegram.warnings import PTBUserWarning

from .handlers import Handler, Handlers

warnings.filterwarnings(
    action="ignore",
    message=".* should be built via the `ApplicationBuilder`",
    category=PTBUserWarning,
)

DEFAULTS = Defaults(
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
)


class App:
    def __init__(self, token: str) -> None:
        builder = Application.builder()
        builder.token(token).defaults(DEFAULTS).concurrent_updates(True)  # noqa: FBT003
        self.raw = builder.build()

    def _add_handler(self, handler: Handler) -> None:
        self.raw.add_handler(handler.build())

    def run(self, handlers: Handlers) -> None:
        for handler in handlers:
            self._add_handler(handler)
        self.raw.run_polling()
