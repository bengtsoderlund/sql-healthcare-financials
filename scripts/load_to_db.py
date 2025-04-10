from pathlib import Path
import sqlite3
import pandas as pd
import gc

#==================================================
#            LOAD DATA TO SQL DATABASE
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts":  # Move up one level
    BASE_DIR = BASE_DIR.parent

# Manage paths
DB_PATH = BASE_DIR / "database" / "MarketData.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

csv_table_pairs = [
    ("stock_prices.csv", "stock_prices"),
    ("annual_earnings.csv", "annual_earnings"),
    ("quarterly_earnings.csv", "quarterly_earnings"),
    ("income_statements.csv", "income_statements"),
    ("balance_sheets.csv", "balance_sheets")
]

# === Clean up potential lingering connections ===
# Only needed if running in an interactive environment like Spyder
try:
    conn.close()
except NameError:
    pass  # conn was never defined

try:
    del conn, cursor
except NameError:
    pass  # conn or cursor were never defined

gc.collect()  # Force garbage collection to help free file locks

# Safely delete the database file if it exists
if DB_PATH.exists():
    DB_PATH.unlink()

# Create and populate new SQLite database
with sqlite3.connect(DB_PATH) as conn:
    for filename, table_name in csv_table_pairs:
        csv_path = BASE_DIR / "data" / filename
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded {table_name} from {filename}")
        else:
            print(f"File not found: {csv_path}")
