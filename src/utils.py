from datetime import datetime

import pandas as pd
import requests
from pandas import DataFrame


def get_xlsx_data(file_name: str) -> DataFrame | list:
    """Считывает данные о транзакциях из xlsx-файла и возвращает список словарей"""
    try:
        xlsx_data_file = pd.read_excel(file_name)
        data_list = xlsx_data_file.apply(
            lambda row: {
                "operation_date": row["Дата операции"],
                "payment_date": row["Дата платежа"],
                "card_number": row["Номер карты"],
                "status": row["Статус"],
                "operation_sum": row["Сумма операции"],
                "operation_cur": row["Валюта операции"],
                "payment_sum": row["Сумма платежа"],
                "payment_cur": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "MCC": row["MCC"],
                "description": row["Описание"],
                "bonus": row["Бонусы (включая кэшбэк)"],
                "invest_bank": row["Округление на инвесткопилку"],
                "rounded_sum": row["Сумма операции с округлением"],
            },
            axis=1,
        )
        new_dict_list = []
        row_index = 0
        for row in data_list:
            new_dict_list.append(data_list[row_index])
            row_index += 1
        return new_dict_list
    except FileNotFoundError:
        return "Файл не найден"


def get_time_greeting(date: str) -> str:
    """Функция выводит приветствие в соответствии с текущим временем"""
    current_time = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    if current_time.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= current_time.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_time.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    return greeting


def get_card_list(transactions: list[dict]) -> list:
    """Функция выводит список номеров карт из списка транзакций"""
    card_list = []
    for transaction in transactions:
        if transaction["card_number"]:
            card_list.append(transaction["card_number"])
    card_list_short = []
    for card in card_list:
        if card not in card_list_short and type(card) is str:
            card_list_short.append(card)
    return card_list_short


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


def get_card_data(date: str, transactions: list[dict]) -> list[dict]:
    """Функция выводит 4 последние цифры карты, общую сумму расходов, сумму кэшбэка"""
    card_list = get_card_list(transactions)
    new_card_list = []
    for card in card_list:
        total_spent = get_total_sum(date, transactions, card)
        new_card_dict = {
            "last_digits": card[1:],
            "total_spent": get_total_sum(date, transactions, card),
            "cashback": get_cashback(total_spent),
        }
        new_card_list.append(new_card_dict)
    return new_card_list


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
