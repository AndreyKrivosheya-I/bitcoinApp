import requests
import time
from datetime import datetime


def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['usd']
    except requests.RequestException as e:
        print("Ошибка при получении данных:", e)
        return None


def get_historical_prices():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': 2  # Должно быть >=2 для получения почасовых данных бесплатно
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'prices' not in data:
            print("Ключ 'prices' не найден в ответе API. Вот что вернулось:")
            print(data)
            return

        prices = data['prices']

        print("🕒 Почасовая цена Биткоина за последние 2 дня:\n")
        print(min(prices))
        for timestamp, price in prices:
            dt = datetime.fromtimestamp(timestamp / 1000)
            print(f'{dt.strftime("%Y-%m-%d %H:%M")} — ${price:.2f}')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")

def main():
    while True:
        price = get_bitcoin_price()
        if price is not None:
            print(f'Текущая цена Биткоина: ${price}')
        else:
            print("Не удалось получить цену.")

        time.sleep(10)  # обновление каждые 10 секунд


if __name__ == '__main__':
    get_historical_prices()
    main()

