from pydantic import Field

from ..k8sbase import K8SBaseModel
from .vm import VirtualMachine


class VirtualMachineList(K8SBaseModel):
    kind: str = Field(pattern=r"^(VirtualMachine)?List$")
    api_version: str = Field(pattern=r"^(kubevirt.io/)?v1$")
    items: list[VirtualMachine]
