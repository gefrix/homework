from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_transaction_to_rub


def make_transaction(amount: str, currency: str) -> dict:
    """Создает тестовую транзакцию с суммой и валютой."""
    return {
        "operationAmount": {
            "amount": amount,
            "currency": {
                "code": currency,
            },
        },
    }


def test_convert_transaction_to_rub_with_rub() -> None:
    """Проверяет возврат рублевой суммы без обращения к API."""
    transaction = make_transaction("100.50", "RUB")

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_transaction_to_rub(transaction)

    assert result == 100.50
    mock_get.assert_not_called()


@pytest.mark.parametrize(
    ("currency", "amount", "api_result", "expected"),
    [
        ("USD", "10.00", 900.0, 900.0),
        ("EUR", "20.00", 2000.0, 2000.0),
    ],
)
def test_convert_transaction_to_rub_with_api(
    currency: str,
    amount: str,
    api_result: float,
    expected: float,
) -> None:
    """Проверяет конвертацию USD и EUR через внешний API."""
    transaction = make_transaction(amount, currency)
    response = Mock()
    response.json.return_value = {"result": api_result}
    response.raise_for_status.return_value = None

    with (
        patch("src.external_api.load_dotenv") as mock_load_dotenv,
        patch("src.external_api.os.getenv", return_value="test_api_key") as mock_getenv,
        patch("src.external_api.requests.get", return_value=response) as mock_get,
    ):
        result = convert_transaction_to_rub(transaction)

    assert result == expected
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_once_with("EXCHANGE_RATES_API_KEY")
    mock_get.assert_called_once()

    request_url = mock_get.call_args.args[0]
    request_kwargs = mock_get.call_args.kwargs

    assert request_url == "https://api.apilayer.com/exchangerates_data/convert"
    assert request_kwargs["headers"] == {"apikey": "test_api_key"}
    assert request_kwargs["params"] == {
        "from": currency,
        "to": "RUB",
        "amount": float(amount),
    }
    assert request_kwargs["timeout"] == 10


def test_convert_transaction_to_rub_without_api_key() -> None:
    """Проверяет ошибку при отсутствии API-ключа."""
    transaction = make_transaction("10.00", "USD")

    with (
        patch("src.external_api.load_dotenv"),
        patch("src.external_api.os.getenv", return_value=None),
        patch("src.external_api.requests.get") as mock_get,
    ):
        with pytest.raises(ValueError, match="EXCHANGE_RATES_API_KEY"):
            convert_transaction_to_rub(transaction)

    mock_get.assert_not_called()


def test_convert_transaction_to_rub_unsupported_currency() -> None:
    """Проверяет ошибку для неподдерживаемой валюты."""
    transaction = make_transaction("10.00", "GBP")

    with pytest.raises(ValueError, match="Unsupported currency"):
        convert_transaction_to_rub(transaction)


def test_convert_transaction_to_rub_without_result_in_response() -> None:
    """Проверяет ошибку при отсутствии результата в ответе API."""
    transaction = make_transaction("10.00", "USD")
    response = Mock()
    response.json.return_value = {"success": True}
    response.raise_for_status.return_value = None

    with (
        patch("src.external_api.load_dotenv"),
        patch("src.external_api.os.getenv", return_value="test_api_key"),
        patch("src.external_api.requests.get", return_value=response),
    ):
        with pytest.raises(ValueError, match="result"):
            convert_transaction_to_rub(transaction)


def test_convert_transaction_to_rub_api_error() -> None:
    """Проверяет проброс ошибки внешнего API."""
    transaction = make_transaction("10.00", "USD")
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("API error")

    with (
        patch("src.external_api.load_dotenv"),
        patch("src.external_api.os.getenv", return_value="test_api_key"),
        patch("src.external_api.requests.get", return_value=response),
    ):
        with pytest.raises(requests.HTTPError):
            convert_transaction_to_rub(transaction)
