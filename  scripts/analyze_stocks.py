import pandas as pd
import os

PROCESSED_DATA_DIR = os.path.join('..', 'data', 'processed')

def load_all_data():
    dfs = []
    for file in os.listdir(PROCESSED_DATA_DIR):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, file))
            df['symbol'] = file.replace('.csv', '')
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def calculate_metrics(df):
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    yearly_return = df.groupby('symbol').apply(lambda x: (x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0])
    volatility = df.groupby('symbol')['daily_return'].std()
    avg_price = df.groupby('symbol')['close'].mean()
    avg_volume = df.groupby('symbol')['volume'].mean()
    return yearly_return, volatility, avg_price, avg_volume

if __name__ == "__main__":
    df = load_all_data()
    yearly_return, volatility, avg_price, avg_volume = calculate_metrics(df)
    print("Top 10 Green Stocks:\n", yearly_return.sort_values(ascending=False).head(10))
    print("Top 10 Red Stocks:\n", yearly_return.sort_values().head(10))
    print("Top 10 Most Volatile Stocks:\n", volatility.sort_values(ascending=False).head(10))

