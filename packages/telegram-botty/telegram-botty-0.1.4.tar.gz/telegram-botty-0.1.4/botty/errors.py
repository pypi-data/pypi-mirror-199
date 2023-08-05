class FieldError(AttributeError):
    def __init__(self, obj: object, field: str) -> None:
        self.obj = obj
        self.field = field

    def __str__(self) -> str:
        return f"No `{self.field}` for `{self.obj}`"
