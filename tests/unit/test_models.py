from typing import Any

import pytest
import yaml

from mtv_parser.models import parse_data
from mtv_parser.models.base import ParserBaseModel


@pytest.mark.parametrize("file", ["examples/vm-plans.yaml", "examples/vms.yaml"])
def test_full_parse(file: str) -> None:
    parsed: ParserBaseModel
    with open(file) as file_handle:
        data = yaml.safe_load(file_handle)
        parsed = parse_data(data)

    assert isinstance(parsed, ParserBaseModel)


def test_model_yaml(yaml_data: Any, model: type, expected: dict[str, Any]) -> None:
    if "raises" in expected:
        with pytest.raises(expected["raises"]):
            model.model_validate(yaml_data)
    else:
        parsed = model.model_validate(yaml_data)
        assert isinstance(parsed, model)

        for attr, value in expected.items():
            assert getattr(parsed, attr) == value
