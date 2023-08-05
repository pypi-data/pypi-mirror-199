from abc import ABC

from botty.types import Query

from .update import UpdateHandler


class QueryHandler(UpdateHandler, ABC):
    async def answer(self, text: str, *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        raw = self.update.callback_query
        if raw is None:
            self._raise_field_error("query")
        return Query(raw)
