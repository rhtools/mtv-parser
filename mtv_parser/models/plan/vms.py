from enum import StrEnum
from typing import Self

from pydantic import Field

from ..base import ParserBaseModel
from ..timed import TimedBaseModel
from .status import PlanStatusCondition, PlanStatusConditionType


class Phase(StrEnum):
    COMPLETED = "Completed"
    PENDING = "Pending"


class Unit(StrEnum):
    MB = "MB"


class PipelineProgress(ParserBaseModel):
    completed: int
    total: int


class PipelineAnnotation(ParserBaseModel):
    unit: Unit


class PipelineName(StrEnum):
    INITIALIZE = "Initialize"
    DISKALLOCATION = "DiskAllocation"
    IMAGECONVERSION = "ImageConversion"
    DISKTRANSFERV2V = "DiskTransferV2v"
    VIRTUALMACHINECREATION = "VirtualMachineCreation"


class PipelineTask(ParserBaseModel):
    name: str
    annotations: PipelineAnnotation | None = None
    progress: PipelineProgress


class PipelineStatus(TimedBaseModel):
    name: PipelineName
    phase: Phase
    tasks: list[PipelineTask] = Field(default_factory=list)
    annotations: PipelineAnnotation | None = None
    progess: PipelineProgress


class VMStatus(TimedBaseModel):
    conditions: list[PlanStatusCondition] = Field(default_factory=list)
    id: str
    name: str
    phase: Phase

    @property
    def succeeded(self: Self) -> bool:
        for condition in self.conditions:
            if condition.type_ == PlanStatusConditionType.SUCCEEDED and condition.status:
                return True
        return False
