from abc import ABC

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    on_command = "start"
