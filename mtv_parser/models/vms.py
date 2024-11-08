from enum import StrEnum
from typing import Self

from pydantic import Field

from .base import K8SRef, ParserBaseModel
from .status import StatusCondition, StatusConditionType
from .timed import TimedBaseModel


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
    conditions: list[StatusCondition]
    id: str
    name: str
    phase: Phase

    @property
    def succeeded(self: Self) -> bool:
        for condition in self.conditions:
            if condition.type_ == StatusConditionType.SUCCEEDED and condition.status:
                return True
        return False


# - completed: "2024-07-01T06:29:48Z"
#         conditions:
#         - category: Advisory
#           durable: true
#           lastTransitionTime: "2024-07-01T06:29:45Z"
#           message: The VM migration has FAILED.
#           status: "True"
#           type: Failed
#         error:
#           phase: ConvertGuest
#           reasons:
#           - Guest conversion failed. See pod logs for details.
#         id: vm-2548588
#         name: sat1cdocn00-qz525
#         phase: Completed
#         pipeline:
#         - completed: "2024-07-01T06:26:58Z"
#           description: Initialize migration.
#           name: Initialize
#           phase: Completed
#           progress:
#             completed: 0
#             total: 1
#           started: "2024-07-01T06:26:11Z"
#         - annotations:
#             unit: MB
#           completed: "2024-07-01T06:27:44Z"
#           description: Allocate disks.
#           name: DiskAllocation
#           phase: Completed
#           progress:
#             completed: 149504
#             total: 149504
#           started: "2024-07-01T06:27:01Z"
#           tasks:
#           - annotations:
#               unit: MB
#             completed: "2024-07-01T06:27:44Z"
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_2.vmdk'
#             phase: Completed
#             progress:
#               completed: 122880
#               total: 122880
#             reason: Transfer completed.
#             started: "2024-07-01T06:27:44Z"
#           - annotations:
#               unit: MB
#             completed: "2024-07-01T06:27:44Z"
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_1.vmdk'
#             phase: Completed
#             progress:
#               completed: 10240
#               total: 10240
#             reason: Transfer completed.
#             started: "2024-07-01T06:27:44Z"
#           - annotations:
#               unit: MB
#             completed: "2024-07-01T06:27:44Z"
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_3.vmdk'
#             phase: Completed
#             progress:
#               completed: 5120
#               total: 5120
#             reason: Transfer completed.
#             started: "2024-07-01T06:27:44Z"
#           - annotations:
#               unit: MB
#             completed: "2024-07-01T06:27:44Z"
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_4.vmdk'
#             phase: Completed
#             progress:
#               completed: 1024
#               total: 1024
#             reason: Transfer completed.
#             started: "2024-07-01T06:27:44Z"
#           - annotations:
#               unit: MB
#             completed: "2024-07-01T06:27:44Z"
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_5.vmdk'
#             phase: Completed
#             progress:
#               completed: 10240
#               total: 10240
#             reason: Transfer completed.
#             started: "2024-07-01T06:27:44Z"
#         - completed: "2024-07-01T06:29:45Z"
#           description: Convert image to kubevirt.
#           error:
#             phase: Running
#             reasons:
#             - Guest conversion failed. See pod logs for details.
#           name: ImageConversion
#           phase: Running
#           progress:
#             completed: 0
#             total: 1
#           started: "2024-07-01T06:27:48Z"
#         - annotations:
#             unit: MB
#           description: Copy disks.
#           name: DiskTransferV2v
#           phase: Pending
#           progress:
#             completed: 0
#             total: 149504
#           tasks:
#           - annotations:
#               unit: MB
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_2.vmdk'
#             progress:
#               completed: 0
#               total: 122880
#           - annotations:
#               unit: MB
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_1.vmdk'
#             progress:
#               completed: 0
#               total: 10240
#           - annotations:
#               unit: MB
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_3.vmdk'
#             progress:
#               completed: 0
#               total: 5120
#           - annotations:
#               unit: MB
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_4.vmdk'
#             progress:
#               completed: 0
#               total: 1024
#           - annotations:
#               unit: MB
#             name: '[VCD-DEV_SAT-OCP-DEV-VX3-002] sat1cdocn00-qz525/sat1cdocn00-qz525_5.vmdk'
#             progress:
#               completed: 0
#               total: 10240
#         - description: Create VM.
#           name: VirtualMachineCreation
#           phase: Pending
#           progress:
#             completed: 0
#             total: 1
#         restorePowerState: "On"
#         started: "2024-07-01T06:26:11Z"
