from collections.abc import Iterator
from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод с карты на карту",
        },
        {
            "id": 594226727,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод организации",
        },
    ]


@pytest.mark.parametrize(
    ("currency", "expected_ids"),
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
    expected_ids: list[int],
) -> None:
    result = list(filter_by_currency(transactions, currency))

    assert [transaction["id"] for transaction in result] == expected_ids


def test_filter_by_currency_empty_list() -> None:
    result = list(filter_by_currency([], "USD"))

    assert result == []


def test_filter_by_currency_returns_iterator(transactions: list[dict[str, Any]]) -> None:
    usd_transactions = filter_by_currency(transactions, "USD")

    assert isinstance(usd_transactions, Iterator)
    assert next(usd_transactions)["id"] == 939719570
    assert next(usd_transactions)["id"] == 142264268


def test_transaction_descriptions(transactions: list[dict[str, Any]]) -> None:
    descriptions = transaction_descriptions(transactions)

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            [{"description": "Первая операция"}, {"description": "Вторая операция"}],
            ["Первая операция", "Вторая операция"],
        ),
        ([{"description": "Одна операция"}], ["Одна операция"]),
        ([], []),
    ],
)
def test_transaction_descriptions_with_different_data(
    data: list[dict[str, Any]],
    expected: list[str],
) -> None:
    assert list(transaction_descriptions(data)) == expected


def test_transaction_descriptions_returns_iterator(transactions: list[dict[str, Any]]) -> None:
    descriptions = transaction_descriptions(transactions)

    assert isinstance(descriptions, Iterator)
    assert next(descriptions) == "Перевод организации"


@pytest.mark.parametrize(
    ("start", "stop", "expected"),
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (42, 42, ["0000 0000 0000 0042"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: list[str]) -> None:
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_format() -> None:
    card_number = next(card_number_generator(1234567890123456, 1234567890123456))

    assert card_number == "1234 5678 9012 3456"
    assert len(card_number) == 19
    assert card_number.count(" ") == 3


def test_card_number_generator_stops_correctly() -> None:
    card_numbers = card_number_generator(1, 1)

    assert next(card_numbers) == "0000 0000 0000 0001"
    with pytest.raises(StopIteration):
        next(card_numbers)


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        (0, 1),
        (1, 10000000000000000),
    ],
)
def test_card_number_generator_invalid_range(start: int, stop: int) -> None:
    with pytest.raises(ValueError):
        next(card_number_generator(start, stop))
