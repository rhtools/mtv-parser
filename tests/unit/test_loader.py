from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from mtv_parser import loader


@pytest.mark.parametrize(
    "files",
    [["singlefile"], ["firstfile", "secondfile", "thirdfile"]],
    ids=["single", "multiple"],
)
def test_load_files(monkeypatch: pytest.MonkeyPatch, files: list[Path]) -> None:
    mock_load_path = MagicMock(loader.load_path)
    mock_load_path.side_effect = lambda x: [MagicMock(name=f"{x}{count}") for count in range(mock_load_path.call_count)]
    monkeypatch.setattr(loader, "load_path", mock_load_path)
    response = loader.load_files(files)
    expected_names = [f"{file}{count}" for idx, file in enumerate(files) for count in range(idx + 1)]
    mock_load_path.assert_has_calls([call(file) for file in files])
    assert len(response) == len(expected_names)
    for idx, mockresponse in enumerate(response):
        assert expected_names[idx] in str(mockresponse)


@pytest.mark.parametrize("path_type", ["file", "dir", "empty"], ids=["file", "dir", "empty"])
def test_load_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, path_type: str) -> None:
    expected_files = []
    match path_type:
        case "file":
            tmp_path = tmp_path / "testfile"
            tmp_path.touch()
            expected_files = [tmp_path]
        case "dir":
            expected_files = [(tmp_path / "file1"), (tmp_path / "file2")]
            (tmp_path / "file1").touch()
            (tmp_path / "file2").touch()
        case "empty":
            pass

    mock_parse_file = MagicMock(loader.parse_file)
    monkeypatch.setattr(loader, "parse_file", mock_parse_file)
    loader.load_path(tmp_path)
    mock_parse_file.assert_has_calls([call(file) for file in expected_files], any_order=True)
