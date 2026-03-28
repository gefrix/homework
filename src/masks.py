from typing import Union


def get_mask_card_number(number: Union[int, str]) -> Union[str]:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    number = str(number)
    return f'{number[:4]} {number[4:6]}** **** {number[-4:]}'


def get_mask_account(number: Union[int, str]) -> Union[str]:
    """Функция принимает на вход номер счета и возвращает его маску"""
    number = str(number)
    return f'**{number[-4:]}'
