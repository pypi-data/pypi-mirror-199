from typing import TypeVar

from .errors import FieldError

T = TypeVar("T")


def listify(obj: T | list[T]) -> list[T]:
    """Return `[obj]` if `obj` is not a list yet."""
    if isinstance(obj, list):
        return obj
    return [obj]


def get_validated_field(obj: object, field: str, value: T | None) -> T:
    """If `value` is None, raise `FieldError`, else return it."""
    if value is None:
        raise FieldError(obj, field)
    return value
