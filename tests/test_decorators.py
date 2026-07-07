from pathlib import Path

import pytest

from src.decorators import log


def test_log_success_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет успешное логирование в консоль."""

    @log()
    def add_numbers(x: int, y: int) -> int:
        """Возвращает сумму двух чисел."""
        return x + y

    result = add_numbers(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert captured.out == "add_numbers ok\n"


def test_log_error_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет логирование ошибки в консоль."""

    @log()
    def divide_numbers(x: int, y: int) -> float:
        """Делит первое число на второе."""
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    captured = capsys.readouterr()

    assert "divide_numbers error" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_success_to_file(tmp_path: Path) -> None:
    """Проверяет успешное логирование в файл."""
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def multiply_numbers(x: int, y: int) -> int:
        """Возвращает произведение двух чисел."""
        return x * y

    result = multiply_numbers(4, 5)

    assert result == 20
    assert log_file.exists()
    assert log_file.read_text(encoding="utf-8") == "multiply_numbers ok\n"


def test_log_error_to_file(tmp_path: Path) -> None:
    """Проверяет логирование ошибки в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def get_item(items: list[int], index: int) -> int:
        """Возвращает элемент списка по индексу."""
        return items[index]

    with pytest.raises(IndexError):
        get_item([1, 2, 3], 10)

    log_text = log_file.read_text(encoding="utf-8")

    assert "get_item error" in log_text
    assert "IndexError" in log_text
    assert "Inputs: ([1, 2, 3], 10), {}" in log_text


def test_log_preserves_function_name() -> None:
    """Проверяет сохранение имени исходной функции."""

    @log()
    def original_function() -> str:
        """Возвращает тестовую строку."""
        return "done"

    assert original_function.__name__ == "original_function"


def test_log_appends_lines_to_file(tmp_path: Path) -> None:
    """Проверяет добавление нескольких строк в лог-файл."""
    log_file = tmp_path / "several_calls.log"

    @log(filename=str(log_file))
    def say_hello(name: str) -> str:
        """Возвращает приветствие с именем."""
        return f"Hello, {name}"

    say_hello("Alex")
    say_hello("Maria")

    assert log_file.read_text(encoding="utf-8") == "say_hello ok\nsay_hello ok\n"


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 2, 3),
        (10, 5, 15),
        (-1, 1, 0),
    ],
)
def test_log_with_parametrize(
    capsys: pytest.CaptureFixture[str],
    x: int,
    y: int,
    expected: int,
) -> None:
    """Проверяет логирование параметризованных вызовов."""

    @log()
    def add_numbers(x: int, y: int) -> int:
        """Возвращает сумму двух чисел."""
        return x + y

    assert add_numbers(x, y) == expected
    captured = capsys.readouterr()

    assert captured.out == "add_numbers ok\n"
