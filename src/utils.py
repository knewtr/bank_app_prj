import datetime
from collections import Counter

import pandas as pd
import requests
from pandas import DataFrame


def get_xlsx_data(excel_path: str) -> DataFrame:
    """Функция выводит данные из xlsx-файла"""
    if excel_path == "":
        excel_data = pd.DataFrame(
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
        return excel_data
    try:
        excel_data = pd.read_excel(excel_path)
        excel_data_no_nan = excel_data.loc[excel_data["Номер карты"].notnull()]
    except Exception as e:
        excel_data = pd.DataFrame()
        return excel_data
    return excel_data_no_nan


def get_time_greeting(date_str: str) -> str:
    """Функция выводит приветствие в соответствии с текущим временем"""
    current_time = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    if current_time.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= current_time.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_time.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    return greeting


def get_total_sum(date_period: str, transactions: list[dict], card_number: str) -> float:
    """Функция выводит общую сумму расходов с заданной карты"""
    month_date = date_period[5:7] + "." + date_period[:4]
    transactions_sum_list = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if transaction["card_number"] == card_number and date[3:] == month_date and transaction["payment_sum"] < 0:
            transactions_sum_list.append(transaction["payment_sum"])
    total_operations_sum = abs(sum(transactions_sum_list))
    return total_operations_sum


def get_cashback(total_sum):
    """Функция рассчитывает процент кэшбэка от общей суммы(1%)"""
    cashback = round(total_sum / 100, 2)
    return cashback


def get_card_data(df_data: DataFrame) -> list[dict]:
    """Функция выводит 4 последние цифры карты, общую сумму расходов, сумму кэшбэка"""
    cards_list = list(Counter(df_data.loc[:, "Номер карты"]))
    cards_data = []
    for card in cards_list:
        j_df_data = df_data.loc[df_data.loc[:, "Номер карты"] == card]
        total_spent = abs(sum(j for j in j_df_data.loc[:, "Сумма операции"] if j < 0))
        cashback = round(total_spent / 100, 2)
        cards_data.append({"last digits": card, "total_spent": total_spent, "cashback": cashback})
    return cards_data


def get_top_transactions(df_data: DataFrame, tr_number=5) -> list[dict]:
    """Функция выводит топ-5 транзакций по сумме платежа"""
    top_transactions_list = []
    df = df_data.loc[::]
    df["amount"] = df.loc[:, "Сумма платежа"].map(float).map(abs)
    sorted_df_data = df.sort_values(by="amount", ascending=False, ignore_index=True)
    for i in range(tr_number):
        date = sorted_df_data.loc[i, "Дата платежа"]
        amount = float(sorted_df_data.loc[i, "amount"])
        category = sorted_df_data.loc[i, "Категория"]
        description = sorted_df_data.loc[i, "Описание"]
        top_transactions_list.append(
            {"date": date, "amount": amount, "category": category, "description": description}
        )
    return top_transactions_list


def filter_by_date(current_date: str, df: DataFrame) -> DataFrame:
    """Функция выводит транзакции с начала месяца и до текущей даты"""
    end_date = datetime.datetime.strptime(current_date, "%d.%m.%Y %H:%M:%S")
    start_date = datetime.datetime.strptime(f"01.{end_date.month}.{end_date.year} 00:00:00", "%d.%m.%Y %H:%M:%S")
    df["Дата"] = df["Дата операции"].map(lambda x: datetime.datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))
    filtered_df = df[(df["Дата"] >= start_date) & (df["Дата"] <= end_date)]
    return filtered_df.iloc[:, :-1]


def get_currency_rates(currency_list: list) -> list[dict]:
    """Функция выводит курсы валют и записывает их в json-файл"""
    currency_rates = []
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    courses = response.json()
    for currency in currency_list:
        currency_rates.append({"currency": currency, "price": courses["Valute"][currency]["Value"]})
    return currency_rates


def get_stock_rates(stocks: list, date="2024-08-08") -> list[dict]:
    """Функция выводит список акций и их стоимость"""
    stock_rates = []
    for stock in stocks:
        j = requests.get(f"https://iss.moex.com/iss/securities/{stock}/aggregates.json?date={date}").json()
        data = [{k: r[i] for i, k in enumerate(j["aggregates"]["columns"])} for r in j["aggregates"]["data"]]
        df_data = pd.DataFrame(data)
        price = round(float((df_data.loc[0, "value"] / df_data.loc[0, "volume"])), 2)
        stock_rates.append({"stock": stock, "price": price})
    return stock_rates
