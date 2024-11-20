import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
import yaml

from mtv_parser import models

from . import const as unit_const


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Dynamically create tests at loadtime.

    Effectively,  this does the same think as the @pytest.mark.parametrize,
    but does it in a function rather than with our usual list expansion technique
    to allow us a little more readability

    Parameters set for test function:
        yaml_data (str): yaml string which is passed to yaml_data fixture for loading
        model (pydantic.BaseModel):  the model class to load the model with
        expected (dict): a dictionary of either expected attributes on the parsed model or expected error.


    Args:
        metafunc (pytest.Metafunc): test function.
    """
    if metafunc.definition.name == "test_model_yaml":
        testvalues: list[tuple[str, type, dict[str, Any]]] = []
        testnames: list[str] = []
        for model_name in unit_const.TEST_MODEL_YAML.keys():
            model_path = model_name.split(".")
            model: Any = models
            for part in model_path:
                logging.info("loading %s from %s", part, model)
                model = getattr(model, part)
            if not issubclass(model, models.ParserBaseModel):
                raise ValueError("Cannot load model %s", model_name)
            test_results = unit_const.TEST_MODEL_RESULTS.get(model_name, dict())
            for test_name, yaml_string in unit_const.TEST_MODEL_YAML.get(model_name, dict()).items():
                testnames.append(f"{model_name}-{test_name}")
                testvalues.append((yaml_string, model, test_results.get(test_name, dict())))

        metafunc.parametrize(
            argnames=["yaml_data", "model", "expected"], argvalues=testvalues, ids=testnames, indirect=["yaml_data"]
        )


@pytest.fixture()
def yaml_data(request: pytest.FixtureRequest) -> Any:
    yaml_string: str = request.param
    return yaml.safe_load(yaml_string)


@pytest.fixture()
def file_string(request: pytest.FixtureRequest) -> Generator[str, None, None]:
    yaml_path: Path = Path(request.param)
    with open(yaml_path, "r") as file:
        yield file.read()
