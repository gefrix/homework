from typing import Any

import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    """Возвращает тестовый список транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
        },
        {
            "id": 3,
            "description": "Открытие вклада",
        },
        {
            "id": 4,
            "description": "Комиссия (5%)",
        },
        {
            "id": 5,
        },
    ]


def test_process_bank_search_exact_match(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет поиск по точной строке."""
    result = process_bank_search(
        transactions,
        "Перевод организации",
    )

    assert [transaction["id"] for transaction in result] == [1]


def test_process_bank_search_is_case_insensitive(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет поиск без учета регистра."""
    result = process_bank_search(
        transactions,
        "пЕрЕвОд ОрГаНиЗаЦиИ",
    )

    assert [transaction["id"] for transaction in result] == [1]


def test_process_bank_search_partial_match(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет поиск по части описания."""
    result = process_bank_search(transactions, "карты")

    assert [transaction["id"] for transaction in result] == [2]


def test_process_bank_search_without_matches(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет пустой результат при отсутствии совпадений."""
    assert process_bank_search(transactions, "Кредит") == []


def test_process_bank_search_with_empty_data() -> None:
    """Проверяет обработку пустого списка."""
    assert process_bank_search([], "Перевод") == []


def test_process_bank_search_with_empty_search(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет обработку пустой строки поиска."""
    assert process_bank_search(transactions, "") == []


def test_process_bank_search_without_description(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет операцию без поля description."""
    result = process_bank_search(transactions, "Перевод")

    assert [transaction["id"] for transaction in result] == [1, 2]


def test_process_bank_search_escapes_regular_expression(
    transactions: list[dict[str, Any]],
) -> None:
    """Проверяет буквальный поиск специальных символов."""
    result = process_bank_search(transactions, "Комиссия (5%)")

    assert [transaction["id"] for transaction in result] == [4]


def test_process_bank_operations_counts_categories() -> None:
    """Проверяет подсчет операций по категориям."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Оплата услуг",
    ]

    result = process_bank_operations(data, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Оплата услуг": 0,
    }


def test_process_bank_operations_with_empty_data() -> None:
    """Проверяет нулевые значения для пустого списка операций."""
    result = process_bank_operations(
        [],
        ["Перевод", "Открытие вклада"],
    )

    assert result == {
        "Перевод": 0,
        "Открытие вклада": 0,
    }


def test_process_bank_operations_with_empty_categories() -> None:
    """Проверяет пустой список категорий."""
    assert (
        process_bank_operations(
            [{"description": "Перевод"}],
            [],
        )
        == {}
    )


def test_process_bank_operations_without_description() -> None:
    """Проверяет операцию без поля description."""
    result = process_bank_operations(
        [{}, {"description": "Перевод"}],
        ["Перевод"],
    )

    assert result == {"Перевод": 1}
    assert type(result) is dict
