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
    """Monkeypatch environment with keys and values from parametrization.

    parameter is expected to be dict[str, str]

    Args:
        request (pytest.FixtureRequest): pytest request fixture
        monkeypatch (pytest.MonkeyPatch): pytest monkeypatch fixture

    Yields:
        None: Uses yield to ensure cleanup runs.
    """
    env: dict[str, str] = request.param
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    yield None
    for name in env.keys():
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def root_command(env: None) -> Generator[BaseCommand, None, None]:
    """Load CLI module and return root group.

    Imports cli module at test execution time to allow for proper loading of environment variables.

    Args:
        env (None): Not actually used, but forces pytest to execute env fixture before this one.

    Yields:
        BaseCommand object, loaded after environment monkeypatching
    """
    if "mtv_parser.cli" in sys.modules:
        del sys.modules["mtv_parser.cli"]
    if "mtv_parser.config" in sys.modules:
        del sys.modules["mtv_parser.config"]
    from mtv_parser.cli import root as cmd

    yield cmd
    if "mtv_parser.cli" in sys.modules:
        del sys.modules["mtv_parser.cli"]
    if "cmd" in sys.modules:
        del sys.modules["cmd"]
    if "mtv_parser.config" in sys.modules:
        del sys.modules["mtv_parser.config"]
