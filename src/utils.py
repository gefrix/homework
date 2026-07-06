import json
from typing import Any


def load_operations_from_json(file_path: str) -> list[dict[str, Any]]:
    """Загружает список финансовых операций из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            operations = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(operations, list):
        return []

    for operation in operations:
        if not isinstance(operation, dict):
            return []

    return operations
