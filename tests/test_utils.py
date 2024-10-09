from unittest.mock import patch

import pytest

from src.utils import (get_card_data, get_currency_rates,
                       get_stock_rates, get_time_greeting,
                       get_top_transactions, get_total_sum)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("01.01.2023 06:05:04", "Доброе утро"),
        ("01.01.2023 13:05:04", "Добрый день"),
        ("01.01.2023 20:05:04", "Добрый вечер"),
        ("01.01.2023 01:05:04", "Доброй ночи"),
    ],
)
def test_get_time_greeting(input_data, expected):
    assert get_time_greeting(input_data) == expected


def test_get_total_sum(transactions):
    assert get_total_sum("2019-09-30", transactions, "*7197") == 678.77
    assert get_total_sum("2019-09-30", transactions, "*4556") == 0


def test_get_card_data(test_transactions):
    assert get_card_data(test_transactions) == [{"last digits": "*7197", "total_spent": 224.89, "cashback": 2.25}]


def test_get_top_transactions(top_5):
    assert get_top_transactions(top_5, 2) == [
        {"date": "31.12.2019", "amount": 17000, "category": "Услуги банка", "description": "Колхоз"},
        {"date": "31.12.2020", "amount": 4575.45, "category": "Фастфуд", "description": "Колхоз"},
    ]


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"Valute": {"EUR": {"Value": 95.1844}}}
    assert get_currency_rates(["EUR"]) == [{"currency": "EUR", "price": 95.1844}]
    mock_get.assert_called_once_with("https://www.cbr-xml-daily.ru/daily_json.js")


@patch("requests.get")
def test_get_stock_rates(mock_get, moex_response):
    mock_get.return_value.json.return_value = moex_response
    assert get_stock_rates(["YDEX"]) == [{"stock": "YDEX", "price": 4.0}]
    mock_get.assert_called_once_with("https://iss.moex.com/iss/securities/YDEX/aggregates.json?date=2024-08-08")
