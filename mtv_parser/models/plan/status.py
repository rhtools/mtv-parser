from enum import StrEnum

from pydantic import Field

from ..status import StatusCondition


class PlanStatusConditionCategory(StrEnum):
    ADVISORY = "Advisory"
    CRITICAL = "Critical"
    ERROR = "Error"
    WARN = "Warn"


class PlanStatusConditionType(StrEnum):
    FAILED = "Failed"
    NETWORKMAPREFNOTVALID = "NetworkMapRefNotValid"
    STORAGEMAPNOTREADY = "StorageMapNotReady"
    STORAGEREFNOTVALID = "StorageRefNotValid"
    SUCCEEDED = "Succeeded"
    VMNOTFOUND = "VMNotFound"


class PlanStatusCondition(StatusCondition):
    category: PlanStatusConditionCategory
    durable: bool | None = Field(default=None)
    type_: PlanStatusConditionType
