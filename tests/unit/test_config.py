import click

from mtv_parser.config import Config


def test_make_extra_settings():
    response = Config._make_extra_options()
    assert len(response.keys()) == 1
    assert "files" in response.keys()
    assert response["files"].get("multiple")
    assert isinstance(response["files"].get("type"), click.Path)
