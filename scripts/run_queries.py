from pathlib import Path
import sqlite3
import pandas as pd

#==================================================
#                 RUN SQL QUERIES
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent

# Set paths
DB_PATH = BASE_DIR / "database" / "MarketData.db"
QUERIES_DIR = BASE_DIR / "queries"
RESULTS_DIR = BASE_DIR / "results"

# Check required files and folders
if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at: {DB_PATH}")

if not QUERIES_DIR.exists():
    raise FileNotFoundError(f"Queries folder not found at: {QUERIES_DIR}")

if not RESULTS_DIR.exists():
    RESULTS_DIR.mkdir(parents=True)

def run_query_with_preview(query_file: str):
    query_path = QUERIES_DIR / query_file

    # Load the SQL query
    with open(query_path, 'r') as file:
        sql = file.read()

    # Print description and SQL code
    print("="*80)
    print(f"QUERY FILE: {query_file}")
    print("="*80, "\n")
    print(sql)
    print("-"*80)
    
    # Connect to database and run query
    with sqlite3.connect(DB_PATH) as conn:
        try:
            df = pd.read_sql_query(sql, conn)
        except Exception as e:
            print(f"Error running {query_file}: {e}")
            raise RuntimeError(f"Error running {query_file}: {e}")

    # Save result
    result_file = query_file.replace(".sql", ".csv")
    result_path = RESULTS_DIR / result_file
    df.to_csv(result_path, index=False)

    # Output preview
    print("\nResult preview:\n")
    print(df.head(), "\n\n")
    
# Create list if all sql queries in query folder 
query_files = [file.name for file in QUERIES_DIR.glob("*.sql")]
    
# Execute all sql queries
for query_file in query_files:
    run_query_with_preview(query_file)
