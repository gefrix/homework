from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations() -> list[dict[str, Any]]:
    """Возвращает список тестовых операций."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2018-06-30T02:08:58.425572",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2020-07-03T18:35:29.512364",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2020-07-03T18:35:29.512364",
        },
        {
            "id": 5,
            "date": "2021-01-01T00:00:00",
        },
    ]


def test_filter_by_state_default(operations: list[dict[str, Any]]) -> None:
    """Проверяет фильтрацию операций по статусу по умолчанию."""
    result = filter_by_state(operations)

    assert [operation["id"] for operation in result] == [1, 3]


@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state_with_different_states(
    operations: list[dict[str, Any]],
    state: str,
    expected_ids: list[int],
) -> None:
    """Проверяет фильтрацию операций по разным статусам."""
    result = filter_by_state(operations, state)

    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_without_matching_state(operations: list[dict[str, Any]]) -> None:
    """Проверяет фильтрацию при отсутствии нужного статуса."""
    result = filter_by_state(operations, "ARCHIVED")

    assert result == []


def test_sort_by_date_descending(operations: list[dict[str, Any]]) -> None:
    """Проверяет сортировку операций по дате по убыванию."""
    result = sort_by_date(operations)

    assert [operation["id"] for operation in result] == [5, 3, 4, 1, 2]


def test_sort_by_date_ascending(operations: list[dict[str, Any]]) -> None:
    """Проверяет сортировку операций по дате по возрастанию."""
    result = sort_by_date(operations, reverse=False)

    assert [operation["id"] for operation in result] == [2, 1, 3, 4, 5]


def test_sort_by_date_with_same_dates(operations: list[dict[str, Any]]) -> None:
    """Проверяет сортировку операций с одинаковыми датами."""
    result = sort_by_date(operations)

    assert [operation["id"] for operation in result[1:3]] == [3, 4]


def test_sort_by_date_with_nonstandard_dates() -> None:
    """Проверяет сортировку операций с нестандартной датой."""
    operations = [
        {"id": 1, "date": "not-a-date"},
        {"id": 2, "date": "2024-01-01"},
    ]

    result = sort_by_date(operations, reverse=False)

    assert [operation["id"] for operation in result] == [2, 1]
