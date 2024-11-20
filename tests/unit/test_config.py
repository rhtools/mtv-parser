import click
import pytest

from mtv_parser.config import Config


def test_make_extra_settings() -> None:
    response = Config._make_extra_options()
    assert len(response.keys()) == 1
    assert "files" in response.keys()
    assert response["files"].get("multiple")
    assert isinstance(response["files"].get("type"), click.Path)


@pytest.mark.parametrize("env", [{"mtv_files": '["testfile"]'}], indirect=True)
@pytest.mark.usefixtures("env")
def test_make_extra_settings_with_env() -> None:
    response = Config._make_extra_options()
    assert len(response.keys()) == 1
    assert "files" in response.keys()
    assert response["files"].get("required") is False
