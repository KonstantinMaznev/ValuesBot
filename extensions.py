import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ConvertionException(f" Невозможно перевести одинаковые валюты {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'He удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f"https://v6.exchangerate-api.com/v6/4951e59dc8f40f2a268ea857/pair/{base_ticker}/{quote_ticker}/{amount}")
        resp = json.loads(r.content)
        new_price = resp["conversion_rate"] * amount
        new_price = round(new_price, 3)
        message = f"Стоимость {amount} {base} в {quote} : {new_price}"
        return message


