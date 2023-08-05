from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .handler import HandlerClass


class Handlers:
    def __init__(self, *items: HandlerClass | Handlers) -> None:
        self.items = items

    def __iter__(self) -> Iterator[HandlerClass]:
        for item in self.items:
            if isinstance(item, Handlers):
                yield from item
            else:
                yield item
