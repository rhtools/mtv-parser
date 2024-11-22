from pydantic import ValidationError

from . import plan, vm
from .base import ParserBaseModel
from .k8sbase import K8SBaseModel
from .plan.status import StatusCondition
from .timed import TimedBaseModel

__all__ = [
    "BaseModel",
    "parse_data",
    "ParserBaseModel",
    "Plan",
    "PlanList",
    "VirtualMachine",
    "VirtualMachineList",
]

BaseModel = K8SBaseModel
Plan = plan.Plan
PlanList = plan.PlanList
VirtualMachine = vm.VirtualMachine
VirtualMachineList = vm.VirtualMachineList
RootModels: list[type[BaseModel]] = [Plan, PlanList, VirtualMachine, VirtualMachineList]
CommonModels: list[type[ParserBaseModel]] = [TimedBaseModel, StatusCondition]


def parse_data(data: dict) -> BaseModel:
    """validate a dict of data as a pydantic model based on BaseModel

    Args:
        data (dict): data to send to validator

    Raises:
        ValueError: if no matching models are found

    Returns:
        BaseModel: Parsed model based on BaseModel
    """
    for model in RootModels:
        try:
            return model.model_validate(data)
        except ValidationError:
            continue
    raise ValueError("Unable to parse document")
