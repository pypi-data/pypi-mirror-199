class FieldError(AttributeError):
    def __init__(self, obj: object, field: str) -> None:
        self.obj = obj
        self.field = field

    def __str__(self) -> str:
        return f"No `{self.field}` for `{self.obj}`"


class CallbackDataError(ValueError):
    def __init__(self, callback_data: object) -> None:
        self.callback_data = callback_data

    def __str__(self) -> str:
        return f"Invalid callback_data: {self.callback_data}"
