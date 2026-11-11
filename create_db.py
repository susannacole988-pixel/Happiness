import sqlite3

DB_NAME = "gateway_revenue.db"

with sqlite3.connect(DB_NAME) as conn:
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS revenue_transfers (
        Transaction_ID TEXT PRIMARY KEY,
        Timestamp TEXT,
        Source_Channel TEXT,
        Destination_Wallet TEXT,
        Network TEXT,
        Asset TEXT,
        Amount_USD REAL,
        Status TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS virtual_cards (
        Card_ID TEXT PRIMARY KEY,
        Timestamp TEXT,
        Provider TEXT,
        Amount_USD REAL,
        Target_Wallet TEXT,
        Status TEXT
    )
    ''')

print(f"Database created/verified: {DB_NAME}")
print("Tables created/verified: revenue_transfers, virtual_cards")
