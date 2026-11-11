import sqlite3
import pandas as pd
import streamlit as st
import datetime

# Streamlit Page Config
st.set_page_config(
    page_title="Gateway Revenue & Virtual Card Portal",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ UI Gateway & Virtual Card Tracker")
st.markdown("Monitor gateway revenue and track virtual-card funding requests.")
st.warning(
    "This app is a local tracking demo only. It does not connect to a card provider, "
    "transfer funds, or issue a virtual card. Verify any provider independently before "
    "sending money, and never enter wallet seed phrases or private keys here."
)

# ---------------------------------------------------------
# DATABASE & DATA LOADING
# ---------------------------------------------------------
DB_FILE = "gateway_revenue.db"


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue_transfers (
                Transaction_ID TEXT PRIMARY KEY,
                Timestamp TEXT,
                Source_Channel TEXT,
                Destination_Wallet TEXT,
                Network TEXT,
                Asset TEXT,
                Amount_USD REAL,
                Status TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS virtual_cards (
                Card_ID TEXT PRIMARY KEY,
                Timestamp TEXT,
                Provider TEXT,
                Amount_USD REAL,
                Target_Wallet TEXT,
                Status TEXT
            );
        """)


init_db()


@st.cache_data(ttl=3)
def load_data():
    with sqlite3.connect(DB_FILE) as conn:
        df_rev = pd.read_sql("SELECT * FROM revenue_transfers", conn)
        df_cards = pd.read_sql("SELECT * FROM virtual_cards", conn)
    return df_rev, df_cards


df_revenue, df_cards = load_data()

# Calculations
total_revenue = df_revenue["Amount_USD"].sum() if not df_revenue.empty else 0.0
total_card_spend = df_cards["Amount_USD"].sum() if not df_cards.empty else 0.0
net_available = total_revenue - total_card_spend
wallet_address = "2L58XpbK2voqKDNYLMGssEgaUP2KJUspRNzYiJhuacBm"

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Gateway Revenue", f"${total_revenue:,.2f} USDC")
col2.metric("Allocated to Cards", f"${total_card_spend:,.2f} USD")
col3.metric("Net Unallocated Revenue", f"${net_available:,.2f} USDC")
col4.metric("Target Wallet", f"{wallet_address[:6]}...{wallet_address[-6:]}")

st.divider()

# ---------------------------------------------------------
# NAVIGATION TABS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["💳 Track Virtual Card Request", "📋 Revenue Ledger"])

with tab1:
    st.subheader("Track a Virtual Card Funding Request")
    st.caption("Record a request locally; this does not create or fund a card.")

    with st.form("card_issuance_form"):
        card_amount = st.number_input(
            "Request Amount ($USD)", min_value=5.0, max_value=1000.0, value=50.0, step=5.0
        )
        spending_purpose = st.selectbox(
            "Spending Category",
            ["Online Shopping", "Software Subscriptions", "Services / Supplies", "Other"]
        )
        submit_btn = st.form_submit_button("Record Funding Request")

    if submit_btn:
        if card_amount > net_available:
            st.error(f"Insufficient unallocated revenue! Available balance: ${net_available:,.2f}.")
        else:
            card_id = f"REQ-{int(datetime.datetime.now().timestamp())}"
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = f"Request recorded — {spending_purpose}; not funded"

            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("""
                    INSERT INTO virtual_cards
                        (Card_ID, Timestamp, Provider, Amount_USD, Target_Wallet, Status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (card_id, now_str, "Not connected", card_amount, wallet_address, status))

            st.success(f"Request recorded: `{card_id}` for ${card_amount:,.2f} USD. No funds were transferred.")
            st.rerun()

    st.subheader("Request History")
    if not df_cards.empty:
        st.dataframe(df_cards, use_container_width=True)
    else:
        st.info("No virtual-card requests recorded yet.")

with tab2:
    st.subheader("📋 Gateway Revenue Ledger")
    if not df_revenue.empty:
        st.dataframe(df_revenue, use_container_width=True)
    else:
        st.info("No gateway revenue transactions logged yet.")
