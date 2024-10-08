import datetime
import json
import logging
import os

from src.utils import (get_card_data, get_currency_rates, get_stock_rates,
                       get_time_greeting, get_top_transactions,
                       filter_by_date, get_xlsx_data)

logger = logging.getLogger("main_page.log")
file_handler = logging.FileHandler("../logs/main_page.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")


def main_page(date: str) -> str:
    """Функция возвращает информацию для главной страницы сайта"""
    df = get_xlsx_data(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx"))
    date_for_stock = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%d")
    with open(PATH) as f:
        data = json.load(f)
    filtered_df = filter_by_date(date, df)
    logger.info("Старт")
    currency_list = data["user_currencies"]
    stocks = data["user_stocks"]
    greeting = get_time_greeting(date)
    card_info = get_card_data(filtered_df)
    top_transactions = get_top_transactions(filtered_df)
    currency_rates = get_currency_rates(currency_list)
    stock_rates = get_stock_rates(stocks, date_for_stock)
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
