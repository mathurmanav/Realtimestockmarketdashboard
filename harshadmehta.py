import streamlit as st
import yfinance as yf
import requests
import pandas as pd


st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")
st.title("📈 Indian Stock Market Dashboard")


st.sidebar.header("Stock Selection")
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g., INFY, TCS, RELIANCE)", "INFY")
exchange = st.sidebar.selectbox("Exchange", ["NSE", "BSE"])
period = st.sidebar.selectbox(
    "Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max"], index=5
)
interval = st.sidebar.selectbox(
    "Interval", ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"], index=6
)

suffix = ".NS" if exchange == "NSE" else ".BO"
ticker_symbol = ticker + suffix

try:
    stock = yf.Ticker(ticker_symbol)

    current_price = stock.history(period="1d")["Close"][0]
    st.metric(label=f"Current Price ({ticker_symbol})", value=f"₹{current_price:.2f}")

    data = stock.history(period=period, interval=interval)
    st.subheader("📊 Price Chart")
    st.line_chart(data["Close"])

    st.subheader("🏢 Company Info")
    info = stock.info

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Name:**", info.get("longName", "N/A"))
        st.write("**Sector:**", info.get("sector", "N/A"))
        st.write("**Industry:**", info.get("industry", "N/A"))
        st.write("**CEO:**", info.get("companyOfficers", [{}])[0].get("name", "N/A"))

    with col2:
        st.write("**Market Cap:**", info.get("marketCap", "N/A"))
        st.write("**Revenue:**", info.get("totalRevenue", "N/A"))
        st.write("**Net Income:**", info.get("netIncomeToCommon", "N/A"))

    st.subheader("💰 Income Statement (Last Years)")
    financials = stock.financials
    st.dataframe(financials)

except Exception as e:
    st.error(f"Error fetching data: {e}")


st.subheader("📰 Latest News")

def get_stock_news(query="stock market"):
    API_KEY = "6fad615bf8d94fd69023939d50ab539e"  # ✅ Your NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        # Check if API returned an error
        if data.get("status") != "ok":
            st.error(f"News API Error: {data.get('message', 'Unknown error')}")
            return []

        return data.get("articles", [])
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# Fetch news based on stock ticker (e.g., INFY → Infosys)
news_articles = get_stock_news(ticker)

if news_articles:
    for article in news_articles[:10]:  # ✅ Show top 10 news
        title = article.get("title", "No Title")
        url = article.get("url", "#")
        desc = article.get("description", "No description available")
        source = article.get("source", {}).get("name", "Unknown")
        published = article.get("publishedAt", "")

        st.markdown(f"### [{title}]({url})")
        st.write(desc)
        st.caption(f"Source: {source} | Published: {published}")
        st.write("---")
else:
    st.warning("No news available at the moment.")
