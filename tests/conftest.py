from pathlib import Path

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
