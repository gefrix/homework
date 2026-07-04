import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def card_data() -> str:
    return "Visa Classic 6831982476737658"


def test_mask_account_card(card_data: str) -> None:
    assert mask_account_card(card_data) == "Visa Classic 6831 98** **** 7658"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card_with_different_data(data: str, expected: str) -> None:
    assert mask_account_card(data) == expected


@pytest.mark.parametrize(
    "data",
    [
        "Visa 12345",
        "Счет 123",
        "Visa Classic",
    ],
)
def test_mask_account_card_with_invalid_data(data: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(data)


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2024-02-29T00:00:00", "29.02.2024"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected


@pytest.mark.parametrize(
    "date",
    [
        "",
        "11.03.2024",
        "not-a-date",
    ],
)
def test_get_date_with_invalid_data(date: str) -> None:
    with pytest.raises(ValueError):
        get_date(date)
