import pytest
from click import BaseCommand
from click.testing import CliRunner

from . import const as e2e_const


@pytest.mark.parametrize(
    ["args", "env", "expected_output"],
    [
        (
            e2e_const.ROOT_TEST_ARGS.get(test_name, list()).copy(),
            e2e_const.ROOT_TEST_ENVS.get(test_name, dict()).copy(),
            e2e_const.ROOT_TEST_OUTPUT.get(test_name),
        )
        for test_name in e2e_const.ROOT_TEST_OUTPUT.keys()
    ],
    ids=e2e_const.ROOT_TEST_OUTPUT.keys(),
    indirect=["env"],
)
@pytest.mark.usefixtures("env")
def test_root(runner: CliRunner, root_command: BaseCommand, args: list[str], expected_output: str) -> None:
    response = runner.invoke(root_command, args)
    assert expected_output in response.output
