import requests
import json
from auth_data import values


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Не возможно конвертировать одинаковые валюты {base}.')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Вы ввели не то значение "{amount}"\nПрочитайте внимательно инструкцию /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[values[base]]
        total_base *= amount

        return total_base