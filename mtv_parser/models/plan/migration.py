from typing import Self

from pydantic import Field

from ..base import K8SRef
from ..status import StatusCondition
from ..timed import TimedBaseModel
from .vms import VMStatus


class MigrationHistory(TimedBaseModel):
    conditions: list[StatusCondition]
    migration: K8SRef
    plan: K8SRef


class MigrationStatus(TimedBaseModel):
    history: list[MigrationHistory] = Field(default_factory=list)
    vms: list[VMStatus] = Field(default_factory=list)

    @property
    def succeeded(self: Self) -> bool:
        return all([vm.succeeded for vm in self.vms])
