import json
import logging
from pathlib import Path
from typing import Any

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)
utils_logger.propagate = False

utils_file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")
utils_file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
utils_file_handler.setFormatter(utils_file_formatter)

if not utils_logger.handlers:
    utils_logger.addHandler(utils_file_handler)


def load_operations_from_json(file_path: str) -> list[dict[str, Any]]:
    """Загружает список финансовых операций из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            operations = json.load(file)
    except FileNotFoundError:
        utils_logger.error("File not found: %s", file_path)
        return []
    except json.JSONDecodeError:
        utils_logger.error("Invalid JSON in file: %s", file_path)
        return []
    except OSError as error:
        utils_logger.error("Error while reading file %s: %s", file_path, error)
        return []

    if not isinstance(operations, list):
        utils_logger.error("JSON data is not a list: %s", file_path)
        return []

    for operation in operations:
        if not isinstance(operation, dict):
            utils_logger.error("JSON list contains non-dictionary item: %s", file_path)
            return []

    utils_logger.debug("Operations were loaded successfully from file: %s", file_path)
    return operations
