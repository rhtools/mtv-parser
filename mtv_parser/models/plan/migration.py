from typing import Self

from pydantic import Field

from ..k8sbase import K8SRef
from ..timed import TimedBaseModel
from .status import PlanStatusCondition
from .vms import VMStatus


class MigrationHistory(TimedBaseModel):
    conditions: list[PlanStatusCondition]
    migration: K8SRef
    plan: K8SRef


class MigrationStatus(TimedBaseModel):
    history: list[MigrationHistory] = Field(default_factory=list)
    vms: list[VMStatus] = Field(default_factory=list)

    @property
    def succeeded(self: Self) -> bool:
        return all([vm.succeeded for vm in self.vms])
