from datetime import timedelta
from typing import Self

from pydantic import Field

from ..base import ParserBaseModel
from ..k8sbase import K8SBaseModel, K8SRef
from .migration import MigrationStatus
from .status import PlanStatusCondition, PlanStatusConditionType


class PlanSpec(ParserBaseModel):
    map_: dict[str, K8SRef] = Field(default_factory=dict)
    provider: dict[str, K8SRef] = Field(default_factory=dict)
    target_namespace: str
    vms: list[dict] = Field(default_factory=dict)


class PlanStatus(ParserBaseModel):
    conditions: list[PlanStatusCondition] = Field(default_factory=list)
    migration: MigrationStatus | None = Field(kw_only=True, default=None)


class Plan(K8SBaseModel):
    kind: str = Field(pattern=r"^Plan$")
    api_version: str = Field(pattern=r"^forklift.konveyor.io/v1(beta1)?$")
    spec: PlanSpec
    status: PlanStatus

    @property
    def duration(self: Self) -> timedelta | None:
        if self.status.migration:
            return self.status.migration.duration
        return None

    @property
    def duration_minutes(self: Self) -> float | None:
        if self.duration:
            return self.duration.total_seconds() / 60
        return None

    @property
    def average_duration(self: Self) -> timedelta | None:
        if self.duration and self.vm_count:
            return self.duration / self.vm_count
        return None

    @property
    def vm_count(self: Self) -> int:
        if self.status.migration:
            return len(self.status.migration.vms)
        return 0

    @property
    def succeeded(self: Self) -> bool:
        if self.status.migration:
            return self.status.migration.succeeded
        for condition in self.status.conditions:
            if condition.type_ == PlanStatusConditionType.SUCCEEDED and condition.status:
                return True
        return False
