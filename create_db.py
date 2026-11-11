import sqlite3

DB_NAME = "gateway_revenue.db"

conn = sqlite3.connect(DB_NAME)
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

conn.commit()
conn.close()

print(f"Database created/verified: {DB_NAME}")
print("Table created: revenue_transfers")
