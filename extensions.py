import requests
import json

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ConvertionException(f" Невозможно перевести одинаковые валюты (base).")

        try:
            quote_ticker = keys[quote]
        except KeyError as e:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError as e:
            raise ConvertionException(f'He удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError as e:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f"https://v6.exchangerate-api.com/v6/4951e59dc8f40f2a268ea857/pair/{base_ticker}/{quote_ticker}/{amount}")
        total_base = json.loads(r.content)[quote_ticker]
        return total_base