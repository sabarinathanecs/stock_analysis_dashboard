import streamlit as st
import pandas as pd
import plotly.express as px
import os

PROCESSED_DATA_DIR = os.path.join('..', 'data', 'processed')
SECTOR_MAP_FILE = os.path.join('..', 'data', 'sector_map.csv')

@st.cache_data
def load_data():
    dfs = []
    for file in os.listdir(PROCESSED_DATA_DIR):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, file))
            df['symbol'] = file.replace('.csv', '')
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def main():
    st.title("Nifty 50 Stock Performance Dashboard")
    df = load_data()
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(['symbol', 'date'], inplace=True)
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    yearly_return = df.groupby('symbol').apply(lambda x: (x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0])
    volatility = df.groupby('symbol')['daily_return'].std()

    st.subheader("Top 10 Green Stocks")
    st.dataframe(yearly_return.sort_values(ascending=False).head(10))

    st.subheader("Top 10 Red Stocks")
    st.dataframe(yearly_return.sort_values().head(10))

    st.subheader("Top 10 Most Volatile Stocks")
    vol_df = volatility.sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(vol_df, x='symbol', y=0, labels={'0': 'Volatility'})
    st.plotly_chart(fig)

    st.subheader("Cumulative Return of Top 5 Performing Stocks")
    top5 = yearly_return.sort_values(ascending=False).head(5).index
    cum_df = df[df['symbol'].isin(top5)].copy()
    cum_df['cum_return'] = cum_df.groupby('symbol')['daily_return'].cumsum()
    fig2 = px.line(cum_df, x='date', y='cum_return', color='symbol')
    st.plotly_chart(fig2)

    if os.path.exists(SECTOR_MAP_FILE):
        sector_map = pd.read_csv(SECTOR_MAP_FILE)
        merged = df.merge(sector_map, on='symbol')
        sector_perf = merged.groupby('sector').apply(lambda x: (x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0])
        fig3 = px.bar(sector_perf.reset_index(), x='sector', y=0, labels={'0': 'Avg Yearly Return'})
        st.subheader("Sector-wise Performance")
        st.plotly_chart(fig3)

    st.subheader("Stock Price Correlation Heatmap")
    pivot = df.pivot(index='date', columns='symbol', values='close')
    corr = pivot.corr()
    fig4 = px.imshow(corr, labels=dict(color="Correlation"))
    st.plotly_chart(fig4)

if __name__ == "__main__":
    main()

