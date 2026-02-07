import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📈 Interactive Stock Market Dashboard")

# ------------------ Load Data ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("stock_L.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ------------------ Sidebar ------------------
st.sidebar.header("🔧 Controls")

stock = st.sidebar.selectbox(
    "Select Stock",
    df["stock"].unique()
)

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(), df["Date"].max()]
)

ma_20 = st.sidebar.checkbox("20 Day Moving Average", True)
ma_50 = st.sidebar.checkbox("50 Day Moving Average")
ma_200 = st.sidebar.checkbox("200 Day Moving Average")

# ------------------ Filter Data ------------------
data = df[
    (df["stock"] == stock) &
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ------------------ Metrics ------------------
latest_close = data["Close"].iloc[-1]
prev_close = data["Close"].iloc[-2]
change = latest_close - prev_close
pct_change = (change / prev_close) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Latest Close", f"{latest_close:.2f}")
col2.metric("Change", f"{change:.2f}", f"{pct_change:.2f}%")
col3.metric("Records", len(data))

# ------------------ Moving Averages ------------------
if ma_20:
    data["MA20"] = data["Close"].rolling(20).mean()
if ma_50:
    data["MA50"] = data["Close"].rolling(50).mean()
if ma_200:
    data["MA200"] = data["Close"].rolling(200).mean()

# ------------------ Price Chart ------------------
fig_price = px.line(
    data,
    x="Date",
    y=["Close"] + [col for col in data.columns if "MA" in col],
    title=f"{stock} Closing Price",
    labels={"value": "Price", "variable": "Legend"}
)

fig_price.update_layout(
    hovermode="x unified",
    template="plotly_dark"
)

st.plotly_chart(fig_price, use_container_width=True)

# ------------------ Volume Chart ------------------
if "Volume" in data.columns:
    fig_volume = px.bar(
        data,
        x="Date",
        y="Volume",
        title="Trading Volume"
    )
    fig_volume.update_layout(template="plotly_dark")
    st.plotly_chart(fig_volume, use_container_width=True)

# ------------------ Raw Data ------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(data)
