import asyncio
import sys
import json
from datetime import datetime, timedelta

import aiohttp


class ExchangeRates:
    BASE_URL_PB = (
        "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5&date="
    )
    BASE_URL_BINANCE = "https://api.binance.com/api/v3/ticker/price?symbol="

    DATE_RANGE = 10

    def __init__(self, currency_codes, crypto_codes):
        self.currency_codes = currency_codes
        self.crypto_codes = crypto_codes
        self.session = aiohttp.ClientSession()

    async def fetch(self, url):
        async with self.session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Error fetching {url}: status code {response.status}")
            return await response.text()

    async def get_exchange_rate(self, url):
        response_text = await self.fetch(url)
        response_json = json.loads(response_text)
        return float(response_json["price"])

    async def get_rates(self, days=10, crypto_code=None):
        if days > self.DATE_RANGE:
            raise ValueError(
                f"Error: The number of days cannot exceed {self.DATE_RANGE}"
            )
        today = datetime.now()
        date_range = [today - timedelta(days=x) for x in range(days)]
        for date in date_range:
            for currency_code in self.currency_codes:
                url = (
                    f'{self.BASE_URL_PB}{date.strftime("%d.%m.%Y")}&ccy={currency_code}'
                )
                response_text = await self.fetch(url)
                response_json = json.loads(response_text)
                for currency in response_json:
                    if currency["ccy"] == currency_code:
                        print(
                            f'{date:%d.%m.%Y},Курс {currency["ccy"]}:\n'
                            f'Продаж {round(float(currency["sale"]), 2)} {currency["base_ccy"]}\n'
                            f'Купівля {round(float(currency["buy"]), 2)} {currency["base_ccy"]}\n'
                        )
            if crypto_code:
                url = f"{self.BASE_URL_BINANCE}{crypto_code}USDT"
                exchange_rate = await self.get_exchange_rate(url)
                print(
                    f"{date:%d.%m.%Y}, Курс {crypto_code}:\n "
                    f"1 {crypto_code} = {exchange_rate} USDT"
                )

    async def close(self):
        await self.session.close()


async def main():
    currency_codes = ["USD", "EUR"]  # валюти за замовчуванням
    crypto_codes = [
        "BTC",
        "ETH",
        "SAND",
        "SOL",
        "DOGE",
    ]  # криптовалюти за замовчуванням
    if len(sys.argv) > 1:
        currency_codes = [code.upper() for code in sys.argv[1:] if code.isalpha()]
        crypto_codes = [code.upper() for code in sys.argv[1:] if code.isnumeric()]
    exchange_rates = ExchangeRates(currency_codes, crypto_codes)
    try:
        while True:
            days = int(input("Введіть кількість днів для виводу курсу валют: "))
            crypto_choice = input(
                "Введіть код криптовалюти для виводу (або натисніть Enter, щоб вивести тільки валюти): "
            )
            if crypto_choice.upper() == "":
                await exchange_rates.get_rates(days)
            elif crypto_choice.upper() not in crypto_codes:
                print(f"Код {crypto_choice} не є підтримуваним криптовалютним кодом")
                continue
            else:
                await exchange_rates.get_rates(days, crypto_choice.upper())
            print("Введіть команду exit, щоб вийти з програми.")
            while True:
                user_input = input()
                if user_input.lower() == "exit":
                    return
                else:
                    try:
                        days = int(user_input)
                        crypto_choice = input(
                            "Введіть код криптовалюти для виводу (або натисніть Enter, щоб вивести тільки валюти): "
                        )
                        if crypto_choice.upper() == "":
                            await exchange_rates.get_rates(days)
                        elif crypto_choice.upper() not in crypto_codes:
                            print(
                                f"Код {crypto_choice} не є підтримуваним криптовалютним кодом"
                            )
                            continue
                        else:
                            await exchange_rates.get_rates(days, crypto_choice.upper())
                        print(
                            """Введіть команду exit, щоб вийти з програми.
Введіть повторно кількість днів для виводу курсу валют"""
                        )
                    except ValueError:
                        print(
                            "Невідома команда. Доступна тільки команда exit та кількість днів для виводу курсу валют."
                        )

    except ValueError as e:
        print(e)
    finally:
        await exchange_rates.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
