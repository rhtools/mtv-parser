from typing import Any

from pydantic import Field, ValidationError, model_validator

from ..base import ParserBaseModel
from ..k8sbase import K8SBaseModel
from .common import RefMatcher, RunStrategy
from .status import VirtualMachineStatus
from .template import VirtualMachineInstanceTemplate
from .volume import DataVolumeTemplate


class VirtualMachineSpec(ParserBaseModel):
    data_volume_templates: list[DataVolumeTemplate] = Field(default_factory=list)
    running: bool | None = Field(default=None)
    run_strategy: RunStrategy | None = Field(default=None)
    instance_type: RefMatcher | None = Field(default=None)
    preference: RefMatcher | None = Field(default=None)
    template: VirtualMachineInstanceTemplate

    @model_validator(mode="before")
    @classmethod
    def running_run_strategy_exclusive(cls: type[ParserBaseModel], data: Any) -> Any:
        if isinstance(data, dict):
            if "running" in data and "runStrategy" in data:
                raise ValueError("running and runStrategy are mutually exclusive")
            if "running" not in data and "runStrategy" not in data:
                data["runStrategy"] = ""
        return data


class VirtualMachine(K8SBaseModel):
    kind: str = Field(pattern=r"^VirtualMachine$")
    api_version: str = Field(pattern=r"^kubevirt.io/v1$")
    spec: VirtualMachineSpec
    status: VirtualMachineStatus
