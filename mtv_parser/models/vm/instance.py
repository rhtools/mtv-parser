from enum import StrEnum

from ..base import ParserBaseModel
from .common import RefMatcher


class VirtualMachineInstanceConditionType(StrEnum):
    PROVISIONING = "Provisioning"
    READY = "Ready"
    SYNCHRONIZED = "Synchronized"
    PAUSED = "Paused"
    AGENTCONNECTED = "AgentConnected"
    ACCESSCREDENTIALSSYNCHRONIZED = "AccessCredentialsSynchronized"
    UNSUPPORTEDAGENT = "AgentVersionNotSupported"
    ISMIGRATABLE = "LiveMigratable"
    VCPUCHANGE = "HotVCPUChange"
    MEMORYCHANGE = "HotMemoryChange"
    VOLUMESCHANGE = "VolumesChange"
    DATAVOLUMESREADY = "DataVolumesReady"
    ISSTORAGELIVEMIGRATABLE = "StorageLiveMigratable"


class VirtualMachineInstanceSpec(ParserBaseModel):
    pass


class VirtualMachineInstanceTypeMatcher(RefMatcher):
    pass
