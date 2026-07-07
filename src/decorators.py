from collections.abc import Callable
from functools import wraps
from typing import Any


def log(filename: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Логирует результат выполнения декорируемой функции в консоль или файл."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Оборачивает функцию логирующим wrapper."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Выполняет функцию и записывает результат в лог."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
            except Exception as error:
                message = f"{func.__name__} error: {type(error).__name__}. Inputs: {args}, {kwargs}"
                write_log(message)
                raise

            write_log(message)
            return result

        return wrapper

    def write_log(message: str) -> None:
        """Записывает сообщение в файл или консоль."""
        if filename:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(message + "\n")
        else:
            print(message)

    return decorator
