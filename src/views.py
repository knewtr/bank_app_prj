import datetime
import json
import logging
import os

from src.utils import (get_card_data, get_currency_rates, get_stock_rates,
                       get_time_greeting, get_top_transactions,
                       get_xlsx_data)

logger = logging.getLogger("main_page.log")
file_handler = logging.FileHandler("main_page.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")


def main_page(date: str) -> str:
    """Функция возвращает информацию для главной страницы сайта"""
    date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%d")
    with open(PATH) as f:
        data = json.load(f)

    logger.info("Старт")
    currency_list = data["user_currencies"]
    stocks = data["user_stocks"]
    logger.info("Конвертируем xlsx-файл в список словарей")
    transactions = get_xlsx_data("../data/operations.xlsx")
    logger.info("Формируем приветствие")
    greeting = get_time_greeting()
    logger.info("Формируем данные о карте")
    card_info = get_card_data(date, transactions)
    logger.info("Формируем топ-5 транзакций")
    top_transactions = get_top_transactions(date, transactions)
    logger.info("Формируем данные о курсах валют")
    currency_rates = get_currency_rates(currency_list)
    logger.info("Формируем данные о стоимости акций")
    stock_rates = get_stock_rates(stocks, date)
    logger.info("Формируем JSON-ответ")
    main_page_info = json.dumps(
        {
            "greeting": greeting,
            "cards": card_info,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_rates,
        }
    )
    return main_page_info
