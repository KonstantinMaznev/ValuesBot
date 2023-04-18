import telebot
import requests
import json

from telebot import TeleBot

TOKEN = "5948700376:AAGZZm1zl5a3cgn2M5fHOPiyYwf4Tlo4cus"

bot: TeleBot = telebot.TeleBot(TOKEN)
keys = dict(евро="EUR", доллар="USD", рубль="RUB")

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ConvertionException(f" Невозможно перевести одинаковые валюты (base).")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'He удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f"https://v6.exchangerate-api.com/v6/4951e59dc8f40f2a268ea857/pair/{base_ticker}/{quote_ticker}/{amount}")
        total_base = json.loads(r.content)[keys[quote_ticker]]
        return total_base



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Достуные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertionException('Слишком много параметров.')
    base, quote, amount = values
    total_base=Converter.get_price(base, quote, amount)
    text = f'Цена {amount} {base} в {quote} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
