from datetime import datetime
from enum import StrEnum

from pydantic import Field

from .base import ParserBaseModel


class ConditionStatus(StrEnum):
    TRUE = "True"
    FALSE = "False"
    UNKNOWN = "Unknown"


class StatusCondition(ParserBaseModel):
    last_transition_time: datetime | None = Field(default=None)
    message: str | None = Field(default=None)
    reason: str | None = Field(default=None)
    status: ConditionStatus
