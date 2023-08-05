from typing import TypeVar

T = TypeVar("T")


def listify(obj: T | list[T]) -> list[T]:
    """Return `[obj]` if `obj` is not a list yet."""
    if isinstance(obj, list):
        return obj
    return [obj]
