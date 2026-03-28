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
