from pydantic import ValidationError

from . import plan
from .base import K8SBaseModel, ParserBaseModel
from .status import StatusCondition
from .timed import TimedBaseModel

__all__ = [
    "BaseModel",
    "parse_data",
    "ParserBaseModel",
    "Plan",
    "PlanList",
]

BaseModel = K8SBaseModel
Plan = plan.Plan
PlanList = plan.PlanList
RootModels: list[type[BaseModel]] = [Plan, PlanList]
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
            return model(**data)
        except ValidationError:
            continue
    raise ValueError("Unable to parse document")
