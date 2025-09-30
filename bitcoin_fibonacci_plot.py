import requests
import pandas as pd
import mplfinance as mpf
from datetime import datetime


def fetch_bitcoin_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc'
    params = {
        'vs_currency': 'usd',
        'days': 7  # 1,7,14 дня, часовые свечи (макс. бесплатный интервал)
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()  # формат: [[timestamp, open, high, low, close], ...]


def prepare_dataframe(raw_data):
    df = pd.DataFrame(raw_data, columns=["Timestamp", "Open", "High", "Low", "Close"])
    df["Date"] = pd.to_datetime(df["Timestamp"], unit='ms')
    df.set_index("Date", inplace=True)
    df.drop("Timestamp", axis=1, inplace=True)
    return df


def calculate_fibonacci_levels(df):
    high = df["High"].max()
    low = df["Low"].min()
    levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]

    fib_levels = {}
    for level in levels:
        price = high - (high - low) * level
        fib_levels[level] = price

    return fib_levels, high, low


def plot_candlestick_chart(df, fib_levels, high, low):
    hlines = [price for price in fib_levels.values()]
    hline_colors = ['gray'] * len(hlines)
    hline_labels = [f'{k:.3f} — ${v:.2f}' for k, v in fib_levels.items()]

    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=f'Bitcoin Candlestick Chart with Fibonacci Levels',
        ylabel='Price (USD)',
        hlines=dict(hlines=hlines, colors=hline_colors, linewidths=1.2, linestyle='--'),
        tight_layout=True,
        datetime_format='%m-%d %H:%M',
        figratio=(14, 7),
        figsize=(12, 6),
    )


def main():
    try:
        raw_data = fetch_bitcoin_data()
        df = prepare_dataframe(raw_data)
        fib_levels, high, low = calculate_fibonacci_levels(df)

        print(f'📈 Max price: ${high:.2f}')
        print(f'📉 Min price: ${low:.2f}')
        print("\n📐 Fibonacci Levels:")
        for level, price in fib_levels.items():
            print(f'{level:.3f} — ${price:.2f}')

        plot_candlestick_chart(df, fib_levels, high, low)

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == '__main__':
    main()
