import csv
from io import StringIO
from typing import Any

import pandas as pd


def read_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            return []

        dialect = csv.Sniffer().sniff(content[:2048], delimiters=",;")
        reader = csv.DictReader(StringIO(content), dialect=dialect)
        return list(reader)
    except (FileNotFoundError, OSError, csv.Error):
        return []


def read_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла."""
    try:
        dataframe = pd.read_excel(file_path)
    except (FileNotFoundError, OSError, ValueError):
        return []

    records = dataframe.to_dict(orient="records")
    return [{str(key): value for key, value in record.items()} for record in records]
