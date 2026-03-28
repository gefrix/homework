from datetime import datetime
from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: Union[str]) -> Union[str]:
    """Принимает строку, содержащую тип и номер карты или счета, и возвращает строку с замаскированным номером"""
    parts = data.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if len(number) == 16:
        masked = get_mask_card_number(number)
    elif len(number) == 20:
        masked = get_mask_account(number)
    else:
        raise ValueError("Неизвестный формат номера")

    return f"{name} {masked}"


def get_date(date: Union[str]) -> Union[str]:
    """Принимает строку, содержающую дату в формате ISO 8601, и возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    return datetime.fromisoformat(date).strftime("%d.%m.%Y")
