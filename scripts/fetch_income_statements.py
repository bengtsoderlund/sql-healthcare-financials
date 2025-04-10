from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import requests
import pandas as pd
import os
import json
import sys


#==================================================
#             FETCH INCOME STATEMENTS
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent

# Manage output paths
output_path = BASE_DIR / "data" / "income_statements.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

# Helper function where integer values are reported as 'None'
def safe_int(val):
    try:
        if val in [None, 'None', '']:
            return 0
        return int(float(val))
    except (ValueError, TypeError):
        return 0

# Load API key from environment variable
load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Stop execution if no API key is found
if not API_KEY or API_KEY == "your_actual_api_key_here":
    print("No valid API key found. Existing income data will be used instead.")
    sys.exit()
    
# Fetch data if API key exists
SYMBOLS = ["JNJ", "PFE", "UNH", "MDT"]
income_statements = []

numeric_fields = [
    "grossProfit", "totalRevenue", "costOfRevenue", "costofGoodsAndServicesSold",
    "operatingIncome", "sellingGeneralAndAdministrative", "researchAndDevelopment",
    "operatingExpenses", "investmentIncomeNet", "netInterestIncome", "interestIncome",
    "interestExpense", "nonInterestIncome", "otherNonOperatingIncome", "depreciation",
    "depreciationAndAmortization", "incomeBeforeTax", "incomeTaxExpense",
    "interestAndDebtExpense", "netIncomeFromContinuingOperations", "comprehensiveIncomeNetOfTax",
    "ebit", "ebitda", "netIncome"
    ]

for SYMBOL in SYMBOLS:
    URL = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={SYMBOL}&apikey={API_KEY}"
    print(f"Fetching income statements for {SYMBOL}...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if response contains valid data
        if "annualReports" not in data:
            print(f"API request failed for {SYMBOL}. Existing income data will be used instead.")
            sys.exit()
            
        print(f"Income statements fetched successfully for {SYMBOL}!")
        
        # Extract income statements
        reports = ["annualReports", "quarterlyReports"]
        for report in reports:
            for report_entry in data[report]:
                symbol = SYMBOL
                report_type = "annual" if report == "annualReports" else "quarterly"
                try:
                    fiscal_date = datetime.strptime(report_entry.get("fiscalDateEnding"), "%Y-%m-%d")
                except (TypeError, ValueError):
                    fiscal_date = None
                
                reported_currency = report_entry.get("reportedCurrency")
                                
                numeric_values = [safe_int(report_entry.get(field)) for field in numeric_fields]
                
                income_statements.append([
                    symbol,
                    report_type,
                    fiscal_date,
                    reported_currency,
                    *numeric_values  # Unpack all numeric values in order
                    ])

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"API request error for {SYMBOL}: {e}. Existing income data will be used instead.")
        sys.exit()

income_statements_df = pd.DataFrame(income_statements, columns=[
    "symbol", 
    "report_type", 
    "fiscal_date", 
    "reported_currency",
    *numeric_fields
    ])        
        
# Save DataFrames to CSV
income_statements_df.to_csv(output_path, index=False)
















