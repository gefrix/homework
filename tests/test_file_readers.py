from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel


def test_read_transactions_from_csv_success() -> None:
    """Проверяет, что транзакции из CSV читаются как список словарей."""
    csv_content = "id,state,amount\n1,EXECUTED,100\n2,CANCELED,200\n"

    with patch("builtins.open", mock_open(read_data=csv_content)) as mocked_open:
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == [
        {"id": "1", "state": "EXECUTED", "amount": "100"},
        {"id": "2", "state": "CANCELED", "amount": "200"},
    ]
    mocked_open.assert_called_once_with("data/transactions.csv", encoding="utf-8")


@pytest.mark.parametrize(
    "side_effect",
    [
        FileNotFoundError,
        OSError,
    ],
)
def test_read_transactions_from_csv_error(side_effect: type[Exception]) -> None:
    """Проверяет, что при ошибке чтения CSV возвращается пустой список."""
    with patch("builtins.open", side_effect=side_effect):
        assert read_transactions_from_csv("missing.csv") == []


def test_read_transactions_from_csv_empty_file() -> None:
    """Проверяет, что для пустого CSV-файла возвращается пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        assert read_transactions_from_csv("empty.csv") == []


def test_read_transactions_from_csv_uses_dict_reader() -> None:
    """Проверяет, что CSV-файл читается через csv.DictReader."""
    reader = Mock()
    reader.return_value = [{"id": "1", "state": "EXECUTED"}]

    with (
        patch("builtins.open", mock_open(read_data="id,state\n1,EXECUTED\n")),
        patch("src.file_readers.csv.DictReader", reader),
    ):
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == [{"id": "1", "state": "EXECUTED"}]
    reader.assert_called_once()


def test_read_transactions_from_excel_success() -> None:
    """Проверяет, что транзакции из Excel читаются как список словарей."""
    dataframe = pd.DataFrame(
        [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "CANCELED", "amount": 200},
        ]
    )

    with patch("src.file_readers.pd.read_excel", return_value=dataframe) as mocked_read_excel:
        result = read_transactions_from_excel("data/transactions_excel.xlsx")

    assert result == [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
    ]
    mocked_read_excel.assert_called_once_with("data/transactions_excel.xlsx")


@pytest.mark.parametrize(
    "side_effect",
    [
        FileNotFoundError,
        OSError,
        ValueError,
    ],
)
def test_read_transactions_from_excel_error(side_effect: type[Exception]) -> None:
    """Проверяет, что при ошибке чтения Excel возвращается пустой список."""
    with patch("src.file_readers.pd.read_excel", side_effect=side_effect):
        assert read_transactions_from_excel("missing.xlsx") == []


def test_read_transactions_from_excel_empty_result() -> None:
    """Проверяет, что для пустой Excel-таблицы возвращается пустой список."""
    dataframe = pd.DataFrame()

    with patch("src.file_readers.pd.read_excel", return_value=dataframe):
        assert read_transactions_from_excel("empty.xlsx") == []


def test_read_transactions_from_csv_with_semicolon_delimiter() -> None:
    """Проверяет чтение CSV-файла с разделителем-точкой с запятой."""
    csv_content = "id;state;amount\n" "1;EXECUTED;100\n" "2;CANCELED;200\n"

    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == [
        {"id": "1", "state": "EXECUTED", "amount": "100"},
        {"id": "2", "state": "CANCELED", "amount": "200"},
    ]
