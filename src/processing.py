from typing import Any, Dict, List


def filter_by_state(operations_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Функция принимает словарь с операциями и ключ 'state'.
    Возвращает новый список словарей, у которых ключ 'state' соответствует указанному значению.
    """
    result = []

    for operation in operations_list:
        if "state" in operation:
            if operation["state"] == state:
                result.append(operation)

    return result


def sort_by_date(operations_list: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Функция принимает список словарей и необязательный параметр, задающий порядок сортировки.
    Возвращает новый отсортированный по дате список
    """
    sorted_operations_list = sorted(operations_list, key=lambda operation: operation["date"], reverse=reverse)
    return sorted_operations_list
