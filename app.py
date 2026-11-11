import sqlite3
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Gateway Revenue & Phantom Tracker",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ UI Gateway & Phantom Tracker")
st.markdown("Real-time monitoring for your Solana-based USDC gateway payouts.")

# Fetch data from local SQLite database
@st.cache_data(ttl=5)
def load_data():
    conn = sqlite3.connect("gateway_revenue.db")
    try:
        df = pd.read_sql("SELECT * FROM revenue_transfers", conn)
    except Exception:
        df = pd.DataFrame(columns=[
            "Transaction_ID", "Timestamp", "Source_Channel", 
            "Destination_Wallet", "Network", "Asset", "Amount_USD", "Status"
        ])
    conn.close()
    return df

df_revenue = load_data()

# Top-level Metric Cards
total_amount = df_revenue["Amount_USD"].sum() if not df_revenue.empty else 0.0
total_txns = len(df_revenue)

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Revenue Tracked", value=f"${total_amount:,.2f} USDC")
col2.metric(label="Total Payout Transactions", value=total_txns)
col3.metric(label="Target Wallet", value="2L58X...huacBm")

st.divider()

# Detailed DataFrame View
st.subheader("📋 Transaction Ledger")
if not df_revenue.empty:
    st.dataframe(df_revenue, use_container_width=True)
else:
    st.info("No transactions logged yet. Run your logging script to populate data.")
