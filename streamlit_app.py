import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Читаем API-ключ из Streamlit Secrets
API_KEY = st.secrets["coinmarketcap"]["api_key"]
#URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
URL = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HEADERS = {"X-CMC_PRO_API_KEY": API_KEY}

def get_crypto_data():
    response = requests.get(URL, headers=HEADERS, params={"convert": "USD"})
    data = response.json()
    return {crypto["symbol"]: crypto["quote"]["USD"]["price"] for crypto in data["data"]}

# Интерфейс Streamlit
st.title("Криптовалютный портфель")

st.sidebar.header("Введите свои активы")
crypto_prices = get_crypto_data()
portfolio = {}

default_coins = ["BTC", "ETH", "BNB", "ADA", "SOL"]

for coin in default_coins:
    amount = st.sidebar.number_input(f"{coin} (количество):", min_value=0.0, format="%.6f", value=0.0)
    portfolio[coin] = amount

# Расчёт стоимости портфеля
total_value = sum(portfolio[coin] * crypto_prices.get(coin, 0) for coin in portfolio)
st.write(f"### Общая стоимость портфеля: **${total_value:,.2f}**")

# Таблица с данными
portfolio_data = pd.DataFrame({
    "Монета": list(portfolio.keys()),
    "Количество": list(portfolio.values()),
    "Цена (USD)": [crypto_prices.get(coin, 0) for coin in portfolio],
    "Общая стоимость (USD)": [portfolio[coin] * crypto_prices.get(coin, 0) for coin in portfolio]
})
st.dataframe(portfolio_data)

# Визуализация
fig = px.pie(portfolio_data, values="Общая стоимость (USD)", names="Монета", title="Распределение портфеля")
st.plotly_chart(fig)
