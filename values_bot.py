import telebot
# import pyTelegramBotAPI
import requests
import json

TOKEN = "5948700376:AAGZZm1zl5a3cgn2M5fHOPiyYwf4Tlo4cus"

bot = telebot.TeleBot(TOKEN)
keys = {
    "евро": "EUR",
    "доллар": 'USD',
    "рубль": 'RUB'
}

class ConvertionException (Exception):

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
    base, quote, amount = message.text.split(" ")
    r = requests.get(f'https://api.exchangeratesapi.io/latest?base={keys[base]}&symbols={keys[quote]}')
    total_base = json.loads(r.content)[keys[quote]]
    text = f'Цена {amount} {base} в {quote}- {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
