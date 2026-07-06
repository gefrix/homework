import json
from pathlib import Path

import pytest

from src.utils import load_operations_from_json


def test_load_operations_from_json_success(tmp_path: Path) -> None:
    file_path = tmp_path / "operations.json"
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    file_path.write_text(json.dumps(operations), encoding="utf-8")

    assert load_operations_from_json(str(file_path)) == operations


def test_load_operations_from_json_file_not_found(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.json"

    assert load_operations_from_json(str(file_path)) == []


@pytest.mark.parametrize(
    "file_content",
    [
        "",
        "{",
        '{"id": 1}',
        '"text"',
        "123",
        "[1, 2, 3]",
    ],
)
def test_load_operations_from_json_invalid_data(tmp_path: Path, file_content: str) -> None:
    file_path = tmp_path / "operations.json"
    file_path.write_text(file_content, encoding="utf-8")

    assert load_operations_from_json(str(file_path)) == []
