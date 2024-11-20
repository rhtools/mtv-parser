import sys
from collections.abc import Generator

import pytest
from click import BaseCommand
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


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
