from botty_core.types import PTBHandler, User
from telegram import ext

from .message_or_query import MessageOrQueryHandler


class MessageHandler(MessageOrQueryHandler):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def build(self) -> PTBHandler:
        return ext.MessageHandler(self.filters, self.handle)

    @property
    def user(self) -> User:
        return self.message.user
