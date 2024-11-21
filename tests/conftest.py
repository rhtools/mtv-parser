from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    rootdir = Path(config.rootdir)
    for item in items:
        mark_name = Path(item.fspath).relative_to(rootdir).parts[1]
        if mark_name:
            item.add_marker(getattr(pytest.mark, mark_name))
            item.add_marker(pytest.mark.xdist_group(mark_name))


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "e2e: mark test as e2e test")


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
