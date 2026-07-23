from pathlib import Path
from typing import Any

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import load_operations_from_json
from src.widget import get_date, mask_account_card

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AVAILABLE_STATUSES = ("EXECUTED", "CANCELED", "PENDING")


def _select_data_source() -> list[dict[str, Any]]:
    """Запрашивает источник данных и загружает транзакции."""
    print("Привет! Добро пожаловать в программу работы " "с банковскими транзакциями.")
    print()
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()

        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return load_operations_from_json(str(DATA_DIR / "operations.json"))

        if choice == "2":
            print("Для обработки выбран CSV-файл.")
            return read_transactions_from_csv(str(DATA_DIR / "transactions.csv"))

        if choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return read_transactions_from_excel(str(DATA_DIR / "transactions_excel.xlsx"))

        print("Выберите пункт 1, 2 или 3.")


def _filter_transactions_by_status(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Запрашивает корректный статус и фильтрует транзакции."""
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: " "EXECUTED, CANCELED, PENDING")

        entered_status = input().strip()
        normalized_status = entered_status.upper()

        if normalized_status in AVAILABLE_STATUSES:
            print("Операции отфильтрованы по статусу " f'"{normalized_status}"')
            return filter_by_state(transactions, normalized_status)

        print(f'Статус операции "{entered_status}" недоступен.')


def _is_yes(answer: str) -> bool:
    """Проверяет положительный ответ пользователя."""
    return answer.strip().casefold() == "да"


def _sort_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Запрашивает необходимость и направление сортировки."""
    print("Отсортировать операции по дате? Да/Нет")

    if not _is_yes(input()):
        return transactions

    print("Отсортировать по возрастанию или по убыванию?")
    sorting_order = input().strip().casefold()
    reverse = sorting_order != "по возрастанию"

    transactions_with_date = [transaction for transaction in transactions if transaction.get("date")]
    transactions_without_date = [transaction for transaction in transactions if not transaction.get("date")]

    return sort_by_date(transactions_with_date, reverse=reverse) + transactions_without_date


def _get_currency_code(transaction: dict[str, Any]) -> str:
    """Возвращает код валюты из вложенного или плоского формата."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency")

        if isinstance(currency, dict):
            code = currency.get("code")
            return "" if code is None else str(code)

    code = transaction.get("currency_code")
    return "" if code is None else str(code)


def _filter_ruble_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """При необходимости оставляет только рублевые транзакции."""
    print("Выводить только рублевые транзакции? Да/Нет")

    if not _is_yes(input()):
        return transactions

    return [transaction for transaction in transactions if _get_currency_code(transaction).upper() == "RUB"]


def _filter_transactions_by_search(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """При необходимости фильтрует транзакции по описанию."""
    print("Отфильтровать список транзакций по определенному " "слову в описании? Да/Нет")

    if not _is_yes(input()):
        return transactions

    print("Введите слово или строку для поиска:")
    search = input().strip()
    return process_bank_search(transactions, search)


def _string_value(value: Any) -> str:
    """Преобразует значение в строку для вывода."""
    if value is None:
        return ""

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _get_amount_and_currency(
    transaction: dict[str, Any],
) -> tuple[str, str]:
    """Извлекает сумму и валюту из вложенного или плоского формата."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        amount = _string_value(operation_amount.get("amount"))
        currency = operation_amount.get("currency")

        if isinstance(currency, dict):
            code = _string_value(currency.get("code"))
            name = _string_value(currency.get("name"))
        else:
            code = ""
            name = ""
    else:
        amount = _string_value(transaction.get("amount"))
        code = _string_value(transaction.get("currency_code"))
        name = _string_value(transaction.get("currency_name"))

    currency_label = "руб." if code.upper() == "RUB" else code or name
    return amount, currency_label


def _mask_requisite(value: Any) -> str:
    """Маскирует реквизиты без падения на неполных данных."""
    requisite = _string_value(value)

    if not requisite:
        return ""

    try:
        return mask_account_card(requisite)
    except ValueError:
        return requisite


def _print_transactions(
    transactions: list[dict[str, Any]],
) -> None:
    """Выводит итоговую выборку транзакций."""
    print("Распечатываю итоговый список транзакций...")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под " "ваши условия фильтрации")
        return

    print()
    print("Всего банковских операций в выборке: " f"{len(transactions)}")
    print()

    for transaction in transactions:
        raw_date = _string_value(transaction.get("date"))

        try:
            formatted_date = get_date(raw_date) if raw_date else ""
        except ValueError:
            formatted_date = raw_date

        description = _string_value(transaction.get("description")) or "Без описания"

        print(f"{formatted_date} {description}".strip())

        sender = _mask_requisite(transaction.get("from"))
        recipient = _mask_requisite(transaction.get("to"))

        if sender and recipient:
            print(f"{sender} -> {recipient}")
        elif sender:
            print(sender)
        elif recipient:
            print(recipient)

        amount, currency = _get_amount_and_currency(transaction)

        if amount:
            print(f"Сумма: {amount} {currency}".rstrip())

        print()


def main() -> None:
    """Связывает загрузку, фильтрацию и вывод транзакций."""
    transactions = _select_data_source()
    transactions = _filter_transactions_by_status(transactions)
    transactions = _sort_transactions(transactions)
    transactions = _filter_ruble_transactions(transactions)
    transactions = _filter_transactions_by_search(transactions)
    _print_transactions(transactions)


if __name__ == "__main__":
    main()
