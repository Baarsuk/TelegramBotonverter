import telebot

from auth_data import TOKEN, mess_start, mess_help, values
from extensions import APIException, Converter


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, mess_start)

    @bot.message_handler(commands=['help'])
    def help_message(message):
        bot.send_message(message.chat.id, mess_help)

    @bot.message_handler(commands=['values'])
    def list_values(message):
        text = 'Список валют:'
        for key in values.keys():
            text = '\n'.join((text, key))
        bot.send_message(message.chat.id, text)

    @bot.message_handler(content_types=['text', ])
    def convert_result(message: telebot.types.Message):
        try:
            elements = message.text.split(' ')

            if len(elements) != 3:
                raise APIException('Вы вели больше или меньше трех параметров.\nПрочитайте внимательно инструкцию /help')

            quote, base, amount = elements
            total_base = Converter.get_price(quote, base, amount)

        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя.\n{e}')

        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')

        else:
            text = f'Цена {amount} {quote} в {base} - {total_base}'
            bot.send_message(message.chat.id, text)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(TOKEN)
