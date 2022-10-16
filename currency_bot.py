import telebot
from config import TOKEN
from extensions import API_server, APIException, APICurrencyException, APIAmountException, APIDiffCurrencyException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def description(message: telebot.types.Message):
    bot.reply_to(message, f'Привет, {message.from_user.full_name}, я конвертер валют\n' \
                          'Напишите запрос в виде:\n' \
                          '<базовая валюта>/<требуемая валюта>/<количество>\n' \
                          '/values - список доступных валют\n' \
                          '/help - справочная информация')

@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    s = ''
    for c in server.get_currencies():
        s += str(c) + '\n'
    bot.send_message(message.chat.id, s)

@bot.message_handler(content_types=['text', ])
def conversion(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split('/')
        if base not in server.exist.keys():
            raise APICurrencyException(base)
        elif quote not in server.exist.keys():
            raise APICurrencyException(quote)
        elif not amount.isdigit() or float(amount) == 0:
            raise APIAmountException(amount)
        elif base == quote:
            raise APIDiffCurrencyException
    except APIException as e:
        bot.send_message(message.chat.id, e)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод')
    else:
        price = server.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f'{amount} {base} в {quote} - {price}')

server = API_server()
server.update_currencies()

bot.polling(none_stop=True)
