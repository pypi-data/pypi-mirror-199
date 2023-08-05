import telegram


class User:
    def __init__(self, raw: telegram.User) -> None:
        self.raw = raw

    @property
    def mention(self) -> str:
        return self.raw.mention_html()
