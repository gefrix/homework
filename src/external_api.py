import os
from typing import Any

import requests
from dotenv import load_dotenv


def convert_transaction_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency}")

    load_dotenv()
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")

    if not api_key:
        raise ValueError("EXCHANGE_RATES_API_KEY is not set")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "result" not in data:
        raise ValueError("API response does not contain result")

    return float(data["result"])
