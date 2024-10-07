import tempfile

import pandas as pd

from src.reports import report, spending_by_category


def test_report(capsys):
    """Тестирует запись в файл после успешного выполнения"""

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        log_file_path = tmp_file.name

    @report(filename=log_file_path)
    def func(x, y):
        return x + y

    func(1, 2)

    with open(log_file_path, "r", encoding="utf-8") as file:
        logs = file.read()

    assert "3" in logs


def test_spending_by_category(transactions_df_test):
    df = pd.DataFrame(
        {
            "Дата платежа": ["01.08.2024", "19.07.2024"],
            "Сумма операции": ["-160.89", "-64.0"],
            "Категория": ["Супермаркеты", "Супермаркеты"],
        }
    )
    assert spending_by_category(transactions_df_test, "Супермаркеты").equals(df)
