import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_number() -> str:
    """Возвращает тестовый номер карты."""
    return "7000792289606361"


def test_get_mask_card_number(card_number: str) -> None:
    """Проверяет маскировку номера карты."""
    assert get_mask_card_number(card_number) == "7000 79** **** 6361"


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        ("7000792289606361", "7000 79** **** 6361"),
        (7000792289606361, "7000 79** **** 6361"),
        ("123456789012", "1234 56** **** 9012"),
        ("12345", "1234 5** **** 2345"),
        ("", " ** **** "),
    ],
)
def test_get_mask_card_number_with_different_values(number: int | str, expected: str) -> None:
    """Проверяет маскировку разных вариантов номера карты."""
    assert get_mask_card_number(number) == expected


def test_get_mask_card_number_without_card_number() -> None:
    """Проверяет маскировку строки без явного номера карты."""
    result = get_mask_card_number("Visa Classic")

    assert result == "Visa  C** **** ssic"


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        ("73654108430135874305", "**4305"),
        (73654108430135874305, "**4305"),
        ("123", "**123"),
        ("", "**"),
    ],
)
def test_get_mask_account(number: int | str, expected: str) -> None:
    """Проверяет маскировку номера счета."""
    assert get_mask_account(number) == expected
