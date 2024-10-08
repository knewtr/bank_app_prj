import pandas as pd
import pytest


@pytest.fixture()
def test_transactions():
    df = pd.DataFrame(
        {
            "Дата операции": ["31.12.2021  16:44:00", "31.12.2021  16:42:04"],
            "Дата платежа": ["31.12.2021", "31.12.2021"],
            "Номер карты": ["*7197", "*7197"],
            "Статус": ["OK", "OK"],
            "Сумма операции": [-160.89, -64],
            "Валюта операции": ["RUB", "RUB"],
            "Сумма платежа": [-160.89, -64],
            "Валюта платежа": ["RUB", "RUB"],
            "Кэшбэк": ["", ""],
            "Категория": ["Супермаркеты", "Супермаркеты"],
            "МСС": ["5411", "5411"],
            "Описание": ["Колхоз", "Колхоз"],
            "Бонусы (включая кэшбэк)": ["3", "1"],
            "Округление на инвесткопилку": ["0", "0"],
            "Сумма операции с округлением": ["160,89", "64"],
        }
    )
    return df


@pytest.fixture()
def empty_df():
    em_df = pd.DataFrame(
        {
            "Дата операции": [],
            "Дата платежа": [],
            "Номер карты": [],
            "Статус": [],
            "Сумма операции": [],
            "Валюта операции": [],
            "Сумма платежа": [],
            "Валюта платежа": [],
            "Кэшбэк": [],
            "Категория": [],
            "МСС": [],
            "Описание": [],
            "Бонусы (включая кэшбэк)": [],
            "Округление на инвесткопилку": [],
            "Сумма операции с округлением": [],
        }
    )
    return em_df


@pytest.fixture
def transactions():
    return [
        {
            "operation_date": "27.09.2019 13:05:37",
            "payment_date": "29.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -144.45,
            "operation_cur": "RUB",
            "payment_sum": -144.45,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Супермаркеты",
            "MCC": 5499.0,
            "description": "Колхоз",
            "Bonus": 2,
            "Invest_bank": 0,
            "rounded_operation_sum": 144.45,
        },
        {
            "operation_date": "27.09.2019 04:17:51",
            "payment_date": "27.09.2019",
            "card_number": "*4556",
            "status": "OK",
            "operation_sum": 1000.0,
            "operation_cur": "RUB",
            "payment_sum": 1000.0,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Бонусы",
            "MCC": 0,
            "description": 'Пополнение. Тинькофф Банк. Бонус по акции "Приведи друга"',
            "Bonus": 0,
            "Invest_bank": 0,
            "rounded_operation_sum": 1000.0,
        },
        {
            "operation_date": "26.09.2019 18:12:45",
            "payment_date": "26.09.2019",
            "card_number": "*4556",
            "status": "OK",
            "operation_sum": 250.0,
            "operation_cur": "RUB",
            "payment_sum": 250.0,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Пополнения",
            "MCC": 0,
            "description": "Пополнение через Альфа-Банк",
            "Bonus": 0,
            "Invest_bank": 0,
            "rounded_operation_sum": 250.0,
        },
        {
            "operation_date": "26.09.2019 17:42:59",
            "payment_date": "28.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -177.1,
            "operation_cur": "RUB",
            "payment_sum": -177.1,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Супермаркеты",
            "MCC": 5411.0,
            "description": "SPAR",
            "Bonus": 3,
            "Invest_bank": 0,
            "rounded_operation_sum": 177.1,
        },
        {
            "operation_date": "26.09.2019 11:57:20",
            "payment_date": "27.09.2019",
            "card_number": "*7197",
            "status": "OK",
            "operation_sum": -357.22,
            "operation_cur": "RUB",
            "payment_sum": -357.22,
            "payment_cur": "RUB",
            "cashback": 0,
            "category": "Отели",
            "MCC": 7011.0,
            "description": "Dongying Luxury Blue Hori",
            "Bonus": 7,
            "Invest_bank": 0,
            "rounded_operation_sum": 357.22,
        },
    ]


@pytest.fixture()
def top_5():
    df = pd.DataFrame(
        {
            "Дата операции": [
                "31.12.2021  16:44:00",
                "31.12.2021  16:42:04",
                "31.12.2020  16:42:04",
                "31.12.2019  16:42:04",
                "31.12.2018  16:42:04",
            ],
            "Дата платежа": ["31.12.2021", "31.12.2021", "31.12.2020", "31.12.2019", "31.12.2018"],
            "Номер карты": ["*7197", "*7197", "*7851", "*7851", "*4521"],
            "Статус": ["OK", "OK", "OK", "OK", "OK"],
            "Сумма операции": ["-160.89", "-64", "-4575.45", "-17000", "-5.05"],
            "Валюта операции": ["RUB", "RUB", "RUB", "RUB", "RUB"],
            "Сумма платежа": ["-160.89", "-64", "-4575.45", "-17000", "-5.05"],
            "Валюта платежа": ["RUB", "RUB", "RUB", "RUB", "RUB"],
            "Кэшбэк": ["", "", "", "", ""],
            "Категория": ["Супермаркеты", "Супермаркеты", "Фастфуд", "Услуги банка", "Переводы"],
            "МСС": ["5411", "5411", "5411", "5411", "5411"],
            "Описание": ["Колхоз", "Колхоз", "Колхоз", "Колхоз", "Колхоз"],
            "Бонусы (включая кэшбэк)": ["3", "1", "", "", ""],
            "Округление на инвесткопилку": ["0", "0", "0", "0", "0"],
            "Сумма операции с округлением": ["160,89", "64", "4575.75", "17000", "5.05"],
        }
    )
    return df


@pytest.fixture()
def moex_response():
    response = {
        "aggregates": {
            "metadata": {
                "market_name": {"type": "string", "bytes": 45, "max_size": 0},
                "market_title": {"type": "string", "bytes": 765, "max_size": 0},
                "engine": {"type": "string", "bytes": 45, "max_size": 0},
                "tradedate": {"type": "date", "bytes": 10, "max_size": 0},
                "secid": {"type": "string", "bytes": 36, "max_size": 0},
                "value": {"type": "double"},
                "volume": {"type": "int64"},
                "numtrades": {"type": "int64"},
                "updated_at": {"type": "datetime", "bytes": 19, "max_size": 0},
            },
            "columns": [
                "market_name",
                "market_title",
                "engine",
                "tradedate",
                "secid",
                "value",
                "volume",
                "numtrades",
                "updated_at",
            ],
            "data": [
                ["shares", "Рынок акций", "stock", "2024 - 08 - 08", "YDEX", 20, 5, 132682, "2024-08-09 00:08:05"],
                [
                    "ndm",
                    "Режим переговорных сделок",
                    "stock",
                    "2024 - 08 - 08",
                    "YDEX",
                    238948.0,
                    62,
                    2,
                    "2024 - 08 - 09 00: 08: 05",
                ],
                [
                    "ccp",
                    "РЕПО с ЦК",
                    "stock",
                    "2024-08-08",
                    "YDEX",
                    6716392432.71,
                    1785300,
                    8462,
                    "2024-08-09 00:08: 05",
                ],
                [
                    "repo",
                    "Рынок сделок РЕПО",
                    "stock",
                    "2024-08-08",
                    "YDEX",
                    6716392432.71,
                    1785300,
                    8462,
                    "2024-08-09 00:08: 05",
                ],
            ],
        },
        "agregates.dates": {
            "metadata": {
                "from": {"type": "date", "bytes": 30, "max_size": 0},
                "till": {"type": "date", "bytes": 30, "max_size": 0},
            },
            "columns": ["from", "till"],
            "data": [["2024 - 05 - 14", "2024 - 08 - 09"]],
        },
    }
    return response


@pytest.fixture()
def operation_list():
    op_list = [
        {"Дата операции": "2018-02-01", "Сумма операции": 90},
        {"Дата операции": "2019-01-01", "Сумма операции": 55},
        {"Дата операции": "2018-02-12", "Сумма операции": 45},
        {"Дата операции": "2019-01-12", "Сумма операции": 41},
    ]
    return op_list


@pytest.fixture()
def transactions_df_test():
    df = pd.DataFrame(
        {
            "Дата платежа": ["01.08.2024", "19.07.2024", "20.06.2024", "31.12.2019", "31.12.2018"],
            "Сумма операции": ["-160.89", "-64.0", "-4575.45", "-17000.0", "-5.05"],
            "Категория": ["Супермаркеты", "Супермаркеты", "Фастфуд", "Ж/Д билеты", "Переводы"],
        }
    )
    return df