from collections.abc import Iterator
from pathlib import Path

import yaml

from mtv_parser.models import BaseModel, parse_data


def load_files(files: list[Path]) -> list[BaseModel]:
    """Parse a list of Path objects into pydantic models.

    Args:
        files (list[Path]): list of Path objects to load

    Returns:
        list[BaseModel]: validated pydantic models
    """
    parsed: list[BaseModel] = []

    for path in files:
        parsed.extend(load_path(path))

    return parsed


def load_path(file: Path) -> list[BaseModel]:
    """parse path objects and call parser on each file.

    Args:
        file (Path): Path Object to process

    Returns:
        list[BaseModel]: validated pydantic models from parser
    """
    parsed: list[BaseModel] = []

    if file.is_dir():
        for path in file.iterdir():
            parsed.extend(load_path(path))
    else:
        parsed.extend(parse_file(file))

    return parsed


def parse_file(file: Path) -> list[BaseModel]:
    """Read a yaml file and parses it into a list of pydantic models.

    Args:
        file (Path): Path object for file to load

    Returns:
        list[BaseModel]: validated pydantic models from parser
    """
    parsed: list[BaseModel] = []

    with open(file) as filedata:
        docs: Iterator[dict] = yaml.safe_load_all(filedata)
        for doc in docs:
            if not isinstance(doc, dict):
                raise ValueError("Yaml Document is not a valid Kubernetes Manifest")
            parsed.append(parse_data(doc))

    return parsed
