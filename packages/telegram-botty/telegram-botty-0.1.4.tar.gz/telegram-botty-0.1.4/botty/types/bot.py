import telegram
from telegram.helpers import create_deep_linked_url


class Bot:
    def __init__(self, raw: telegram.Bot) -> None:
        self.raw = raw

    def get_start_url(self, payload: str = "0", *, group: bool = False) -> str:
        username = self.raw.username
        return create_deep_linked_url(username, payload, group)

    @property
    def start_url(self) -> str:
        return self.get_start_url()

    @property
    def startgroup_url(self) -> str:
        return self.get_start_url(group=True)
