from abc import ABC

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    def __init__(self) -> None:
        super().__init__("start")
