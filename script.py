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
        'days': 2
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()['prices']

        min_point = min(data, key=lambda x: x[1])
        max_point = max(data, key=lambda x: x[1])

        min_price = min_point[1]
        max_price = max_point[1]

        min_dt = datetime.fromtimestamp(min_point[0] / 1000)
        max_dt = datetime.fromtimestamp(max_point[0] / 1000)

        print("🕒 Почасовая цена Биткоина за последние 2 дня:\n")
        for timestamp, price in data:
            dt = datetime.fromtimestamp(timestamp / 1000)
            print(f'{dt.strftime("%Y-%m-%d %H:%M")} — ${price:.2f}')

        print(f"\n📉 Минимум: {min_dt.strftime('%Y-%m-%d %H:%M')} — ${min_price:.2f}")
        print(f"📈 Максимум: {max_dt.strftime('%Y-%m-%d %H:%M')} — ${max_price:.2f}")

        # === Построение уровней Фибоначчи ===
        fib_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        print("\n📐 Уровни Фибоначчи:")

        for level in fib_levels:
            price_level = max_price - (max_price - min_price) * level
            print(f"Уровень {level:.3f}: ${price_level:.2f}")

    except Exception as e:
        print("Ошибка при получении исторических данных:", e)



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

