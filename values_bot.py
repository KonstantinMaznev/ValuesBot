import telebot
import traceback
from config import keys, TOKEN
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)


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
    try:
        if len(values) != 3:
            raise ConvertionException('Слишком много или мало параметров.')
        base, quote, amount = values
        total_base = Converter.get_price(*values)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        bot.reply_to(message, total_base)


bot.polling(none_stop=True)
