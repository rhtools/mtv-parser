from datetime import datetime, timedelta
from typing import Self

from pydantic import Field

from .base import ParserBaseModel


class TimedBaseModel(ParserBaseModel):
    started: datetime | None = Field(default=None)
    completed: datetime | None = Field(default=None)

    @property
    def duration(self: Self) -> timedelta | None:
        if self.started and self.completed:
            return self.completed - self.started
        return None
