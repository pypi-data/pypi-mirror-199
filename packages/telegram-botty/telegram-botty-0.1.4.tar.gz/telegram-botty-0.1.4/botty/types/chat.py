import telegram


class Chat:
    def __init__(self, raw: telegram.Chat) -> None:
        self.raw = raw

    @property
    def is_private(self) -> bool:
        return self.raw.type == self.raw.PRIVATE

    @property
    def is_group(self) -> bool:
        return self.raw.type in [self.raw.GROUP, self.raw.SUPERGROUP]
