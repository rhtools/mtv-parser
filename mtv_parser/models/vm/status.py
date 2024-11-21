from datetime import datetime
from enum import StrEnum

from pydantic import Field

from ..base import ParserBaseModel
from ..status import StatusCondition
from .common import RunStrategy
from .instance import VirtualMachineInstanceConditionType


class VMConditionType(StrEnum):
    FAILURE = "Failure"
    READY = "Ready"
    PAUSED = "Paused"
    RESTARTREQUIRED = "RestartRequired"
    MANUALRESTARTREQUIRED = "ManualRecoveryRequired"
    INITIALIZED = "Initialized"  # Not found in spec, but exists in real world examples, source unknown


class PrintableStatus(StrEnum):
    STOPPED = "Stopped"
    PROVISIONING = "Provisioning"
    STARTING = "Starting"
    RUNNING = "Running"
    PAUSED = "Paused"
    STOPPING = "Stopping"
    TERMINATING = "Terminating"
    CRASHLOOPBACKOFF = "CrashLoopBackOff"
    MIGRATING = "Migrating"
    UNKNOWN = "Unknown"
    UNSCHEDULABLE = "ErrorUnschedulable"
    ERRIMAGEPULL = "ErrImagePull"
    IMAGEPULLBACKOFF = "ImagePullBackOff"
    PVCNOTFOUND = "ErrorPvcNotFound"
    DATAVOLUMEERROR = "DataVolumeError"
    WAITINGFORVOLUMEBINDING = "WaitingForVolumeBinding"


class VirtualMachineCondition(StatusCondition):
    type_: VMConditionType | VirtualMachineInstanceConditionType
    last_probe_time: datetime | None = Field(default=None)


class VirtualMachineStatus(ParserBaseModel):
    conditions: list[VirtualMachineCondition] = Field(default_factory=list)
    created: bool | None = Field(default=None)
    ready: bool | None = Field(default=None)
    run_strategy: RunStrategy = Field(default=RunStrategy.UNKNOWN)
    printable_status: PrintableStatus = Field(default=PrintableStatus.UNKNOWN)
