import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Возвращает операции, содержащие строку поиска в описании."""
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [operation for operation in data if pattern.search(str(operation.get("description", "")))]


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитывает количество операций для каждой переданной категории."""
    description_counter: Counter[str] = Counter()

    for operation in data:
        description = operation.get("description")

        if isinstance(description, str):
            description_counter[description] += 1

    return {category: description_counter[category] for category in categories}
