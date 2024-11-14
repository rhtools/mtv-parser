import sys
from typing import Any, Generator

import pytest
from click import BaseCommand
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def env(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> Generator[None, Any, None]:
    env: dict[str, str] = request.param
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    yield None
    for name in env.keys():
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def root_command(env: None) -> Generator[BaseCommand, None, None]:
    from mtv_parser.cli import root as cmd

    yield cmd
    del sys.modules["mtv_parser.cli"]
    del sys.modules["cmd"]
