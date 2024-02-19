import telebot

from config import TOKEN, CURRENCIES
from extensions import ConvertionExseption, CurrencyConvertor


bot = telebot.TeleBot(TOKEN)  # Создаем бот


# Отображение инструкций
@bot.message_handler(commands=['start', 'help'])
def commands_help_start(massage: telebot.types.Message):
    text = "<количество валюты, цену которой нужно узнать>\
    <имя валюты, цену которой нужно узнать>\
    <имя валюты, в которой надо узнать цену первой валюты>\n\
    <список доступных волют команда: /values> "
    bot.reply_to(massage, text)


# Доступные валюты
@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = "Доступные валюты "
    for currency in CURRENCIES:
        text = '\n'.join((text, currency))
    bot.reply_to(massage, text)


# Конвертация валют
@bot.message_handler(content_types=['text'])
def convert(massage: telebot.types.Message):
    try:
        value = massage.text.split(' ')
        print(type(value))
        if len(value) != 3:
            raise ConvertionExseption("Слишком много/мало параметров")
        amount, currency, base_currency = value
        value_cur = CurrencyConvertor.convert(currency, base_currency, amount)
    except ConvertionExseption as e:
        bot.reply_to(massage, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(massage, f"Не удалось обработать команду\n{e}")
    else:
        bot.send_message(massage.chat.id, f"{amount} {currency} в {base_currency} = {value_cur}")


bot.polling()
