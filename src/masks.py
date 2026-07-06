import logging
from pathlib import Path
from typing import Union

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)
masks_logger.propagate = False

masks_file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")
masks_file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
masks_file_handler.setFormatter(masks_file_formatter)

if not masks_logger.handlers:
    masks_logger.addHandler(masks_file_handler)


def get_mask_card_number(number: Union[int, str]) -> Union[str]:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    try:
        number = str(number)
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        masks_logger.debug("Card number was masked successfully")
        return masked_number
    except Exception as error:
        masks_logger.error("Error while masking card number: %s", error)
        raise


def get_mask_account(number: Union[int, str]) -> Union[str]:
    """Функция принимает на вход номер счета и возвращает его маску."""
    try:
        number = str(number)
        masked_number = f"**{number[-4:]}"
        masks_logger.debug("Account number was masked successfully")
        return masked_number
    except Exception as error:
        masks_logger.error("Error while masking account number: %s", error)
        raise
