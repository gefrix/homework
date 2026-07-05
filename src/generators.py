from collections.abc import Iterator
from typing import Any


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Возвращает транзакции, у которых код валюты совпадает с заданным."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Возвращает описания транзакций по одному."""
    for transaction in transactions:
        yield str(transaction["description"])


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт от start до stop включительно."""
    min_card_number = 1
    max_card_number = 9999999999999999

    if start < min_card_number or stop > max_card_number:
        raise ValueError("Номер карты должен быть от 1 до 9999999999999999")

    for number in range(start, stop + 1):
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
