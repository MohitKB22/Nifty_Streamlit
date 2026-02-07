import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Page config
st.set_page_config(page_title="Stock Price Viewer", layout="wide")

st.title("📈 Stock Closing Price Viewer")

# Load data
df = pd.read_csv("stock_L.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Stock selector
stock_list = df["stock"].unique()
st.sidebar.header("Select Stock")
st_name = st.sidebar.selectbox("Stock Name", stock_list)

# Filter data
r = df[df["stock"] == st_name]

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
sb.lineplot(data=r, x="Date", y="Close", ax=ax)
ax.set_title(f"Closing Price of {st_name}")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")

st.pyplot(fig)
