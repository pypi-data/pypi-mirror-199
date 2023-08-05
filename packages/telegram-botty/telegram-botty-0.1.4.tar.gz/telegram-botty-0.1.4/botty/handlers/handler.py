from abc import abstractmethod

from .types import PTBHandler


class Handler:
    @classmethod
    @abstractmethod
    def build(cls) -> PTBHandler:
        """Return PTB-compatible handler."""

    @classmethod
    def _validate_class_field(cls, field: str) -> None:
        if getattr(cls, field, None) is None:
            raise HandlerFieldError(cls, field)

    def _validate_field(self, field: str) -> None:
        if getattr(self, field, None) is None:
            raise HandlerFieldError(self.__class__, field)


HandlerClass = type[Handler]


class HandlerFieldError(AttributeError):
    def __init__(self, handler: HandlerClass, field: str) -> None:
        self.handler = handler
        self.field = field

    def __str__(self) -> str:
        return f"You must set `{self.field}` for {self.handler}"
