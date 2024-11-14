import pytest
import yaml

from mtv_parser.models import PlanList
from mtv_parser.models.base import ParserBaseModel


@pytest.mark.parametrize("file", ["examples/vm-plans.yaml"])
def test_parse(file: str) -> None:
    parsed: ParserBaseModel
    with open(file) as file_handle:
        data = yaml.safe_load(file_handle)
        parsed = PlanList(**data)

    assert isinstance(parsed, ParserBaseModel)
