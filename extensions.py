"""
Модуль содержит основной класс, выполняющий запросы к API,
и пользовательские классы исключений
"""

import requests
import json
import time

class API_server:
    def __init__(self):
        self.all = {'евро': 'EUR',
                    'доллар': 'USD',
                    'рубль': 'RUB',
                    'фунт стерлингов': 'GBP',
                    'биткоин': 'BTC'}
        self.exist = {}
        self.time = time.time()
        self.data = {}

    def request(self):
        if (time.time() - self.time) >= 1: #Проверка соответствия требованиям api - запрос не чаще 5 раз в секунду
            self.time = time.time()
            self.data = json.loads(requests.get('https://www.cbr-xml-daily.ru/daily_json.js').content)['Valute']
        return self.data

    def update_currencies(self):
        time.sleep(1)
        data = self.request()
        for v in data:
            for k in self.all.keys():
                if v == self.all[k]:
                    self.exist[k] = v
        self.exist['рубль'] = self.all['рубль']

    def get_currencies(self):
        return [k for k in self.exist.keys()]

    def get_price(self, base, quote, amount):
        data = self.request()
        if base == 'рубль':
            result = 1 / (data[self.exist[quote]]['Value'] / data[self.exist[quote]]['Nominal']) * float(amount)
        elif quote == 'рубль':
            result = (data[self.exist[base]]['Value'] / data[self.exist[base]]['Nominal']) * float(amount)
        else:
            result = (data[self.exist[base]]['Value'] / data[self.exist[base]]['Nominal']) / \
                     (data[self.exist[quote]]['Value'] / data[self.exist[quote]]['Nominal']) * float(amount)
        return result

class APIException(Exception):
    def __init__(self, message):
        super().__init__(message)

class APIAmountException(APIException):
    def __init__(self, amount):
        super().__init__(f"Неверное количество '{amount}'")

class APICurrencyException(APIException):
    def __init__(self, currency):
        super().__init__(f"Недоступная валюта '{currency}'")

class APIDiffCurrencyException(APIException):
    def __init__(self):
        super().__init__("Введите разные валюты")
