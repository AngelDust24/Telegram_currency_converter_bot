import requests

import json

from config import CURRENCIES, API_KEY


class ConvertionExseption(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def convert(currency, base_currency, amount):
        if currency == base_currency:
            raise ConvertionExseption(f"Не удалось перевести одинаковые валюты {currency}")
        try:
            cur = CURRENCIES[currency]
        except KeyError:
            raise ConvertionExseption(f"Не удалось обработать валюту {currency}")

        try:
            base_cur = CURRENCIES[base_currency]
        except KeyError:
            raise ConvertionExseption(f"Не удалось обработать валюту {base_currency}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExseption(f"Не удалось обработать колличество {amount}")

        r = requests.get(f"https://currate.ru/api/?get=rates&pairs={cur}{base_cur}&key={API_KEY}")
        value_cur = json.loads(r.content)["data"][f"{CURRENCIES[currency]}{CURRENCIES[base_currency]}"]
        return round(float(value_cur) * amount, 10)
