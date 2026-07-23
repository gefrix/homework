from typing import Any
from unittest.mock import patch

import pytest

from src.main import main


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    """Возвращает транзакции для тестирования консольного интерфейса."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T00:00:00",
            "description": "Открытие вклада",
            "to": "Счет 12345678901234564321",
            "operationAmount": {
                "amount": "40542",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-11-12T00:00:00",
            "description": "Перевод с карты на карту",
            "from": "MasterCard 7771271234563727",
            "to": "Visa Platinum 1293381234569203",
            "operationAmount": {
                "amount": "130",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2018-07-18T00:00:00",
            "description": "Перевод организации",
            "to": "Счет 12345678901234560034",
            "operationAmount": {
                "amount": "8390",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
        },
    ]


@pytest.mark.parametrize(
    ("choice", "reader_name", "expected_message"),
    [
        (
            "1",
            "load_operations_from_json",
            "Для обработки выбран JSON-файл.",
        ),
        (
            "2",
            "read_transactions_from_csv",
            "Для обработки выбран CSV-файл.",
        ),
        (
            "3",
            "read_transactions_from_excel",
            "Для обработки выбран XLSX-файл.",
        ),
    ],
)
def test_main_selects_data_source(
    choice: str,
    reader_name: str,
    expected_message: str,
    transactions: list[dict[str, Any]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет выбор каждого источника данных."""
    answers = [choice, "EXECUTED", "нет", "нет", "нет"]

    with (
        patch("builtins.input", side_effect=answers),
        patch(
            f"src.main.{reader_name}",
            return_value=transactions,
        ) as mocked_reader,
    ):
        main()

    output = capsys.readouterr().out

    assert expected_message in output
    assert "Всего банковских операций в выборке: 2" in output
    mocked_reader.assert_called_once()


def test_main_repeats_status_request(
    transactions: list[dict[str, Any]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет повторный запрос после некорректного статуса."""
    answers = [
        "1",
        "test",
        "Executed",
        "нет",
        "нет",
        "нет",
    ]

    with (
        patch("builtins.input", side_effect=answers),
        patch(
            "src.main.load_operations_from_json",
            return_value=transactions,
        ),
    ):
        main()

    output = capsys.readouterr().out

    assert 'Статус операции "test" недоступен.' in output
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in output


def test_main_handles_empty_selection(
    transactions: list[dict[str, Any]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет сообщение для пустой итоговой выборки."""
    answers = ["1", "EXECUTED", "нет", "нет", "нет"]

    with (
        patch("builtins.input", side_effect=answers),
        patch(
            "src.main.load_operations_from_json",
            return_value=[transactions[2]],
        ),
    ):
        main()

    output = capsys.readouterr().out

    assert ("Не найдено ни одной транзакции, подходящей под " "ваши условия фильтрации") in output


def test_main_applies_all_optional_filters(
    transactions: list[dict[str, Any]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет сортировку, валютный фильтр и поиск."""
    answers = [
        "1",
        "EXECUTED",
        "да",
        "по возрастанию",
        "да",
        "да",
        "вклада",
    ]

    with (
        patch("builtins.input", side_effect=answers),
        patch(
            "src.main.load_operations_from_json",
            return_value=transactions,
        ),
    ):
        main()

    output = capsys.readouterr().out

    assert "Всего банковских операций в выборке: 1" in output
    assert "08.12.2019 Открытие вклада" in output
    assert "Счет **4321" in output
    assert "Сумма: 40542 руб." in output
    assert "Сумма: 130 USD" not in output


def test_main_repeats_invalid_source_choice(
    transactions: list[dict[str, Any]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет повторный запрос при неверном пункте меню."""
    answers = [
        "9",
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ]

    with (
        patch("builtins.input", side_effect=answers),
        patch(
            "src.main.load_operations_from_json",
            return_value=transactions,
        ),
    ):
        main()

    output = capsys.readouterr().out

    assert "Выберите пункт 1, 2 или 3." in output
    assert "Для обработки выбран JSON-файл." in output
