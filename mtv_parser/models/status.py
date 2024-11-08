from datetime import datetime
from enum import StrEnum

from .base import ParserBaseModel


class StatusConditionCategory(StrEnum):
    ADVISORY = "Advisory"
    CRITICAL = "Critical"
    ERROR = "Error"
    WARN = "Warn"


class StatusConditionType(StrEnum):
    FAILED = "Failed"
    NETWORKMAPREFNOTVALID = "NetworkMapRefNotValid"
    STORAGEMAPNOTREADY = "StorageMapNotReady"
    STORAGEREFNOTVALID = "StorageRefNotValid"
    SUCCEEDED = "Succeeded"
    VMNOTFOUND = "VMNotFound"


class StatusCondition(ParserBaseModel):
    category: StatusConditionCategory
    durable: bool | None = None
    lastTransitionTime: datetime
    message: str
    status: bool = True
    type_: StatusConditionType
