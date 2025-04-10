from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import requests
import pandas as pd
import os
import json
import sys


#==================================================
#              FETCH EARNINGS
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent

# Manage output paths
annual_earnings_path = BASE_DIR / "data" / "annual_earnings.csv"
annual_earnings_path.parent.mkdir(parents=True, exist_ok=True)

quarterly_earnings_path = BASE_DIR / "data" / "quarterly_earnings.csv"
quarterly_earnings_path.parent.mkdir(parents=True, exist_ok=True)

# Load API key from environment variable
load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Stop execution if no API key is found
if not API_KEY or API_KEY == "your_actual_api_key_here":
    print("No valid API key found. Existing earnings data will be used instead.")
    sys.exit()
    
# Fetch data if API key exists
SYMBOLS = ["JNJ", "PFE", "UNH", "MDT"]
annual_earnings = []
quarterly_earnings = []

for SYMBOL in SYMBOLS:
    URL = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={SYMBOL}&apikey={API_KEY}"
    print(f"Fetching earnings for {SYMBOL}...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if response contains valid data
        if "annualEarnings" not in data:
            print(f"API request failed for {SYMBOL}. Existing earnings data will be used instead.")
            sys.exit()
            
        print(f"Earnings fetched successfully for {SYMBOL}!")
        
        # Extract annual earnings
        for earnings_entry in data["annualEarnings"]:
            symbol = SYMBOL
            fiscal_year = datetime.strptime(earnings_entry["fiscalDateEnding"], "%Y-%m-%d")
            eps = float(earnings_entry["reportedEPS"])
            annual_earnings.append([symbol, fiscal_year, eps])
            
        # Extract querterly earnings
        for earnings_entry in data["quarterlyEarnings"]:
            symbol = SYMBOL
            fiscal_quarter = datetime.strptime(earnings_entry["fiscalDateEnding"], "%Y-%m-%d")
            date_reported = datetime.strptime(earnings_entry["reportedDate"], "%Y-%m-%d")
            reported_eps = float(earnings_entry["reportedEPS"])
            estimated_eps = float(earnings_entry["estimatedEPS"])
            surprise = float(earnings_entry["surprise"])
            surprise_pct = float(earnings_entry["surprisePercentage"])
            report_time = earnings_entry["reportTime"]
            quarterly_earnings.append([symbol, fiscal_quarter, date_reported, reported_eps, estimated_eps, surprise, surprise_pct, report_time])
        
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"API request error for {SYMBOL}: {e}. Existing earnings data will be used instead.")
        sys.exit()
        
annual_earnings_df = pd.DataFrame(annual_earnings, columns=["symbol", "fiscal_year", "reported_EPS"])
quarterly_earnings_df = pd.DataFrame(quarterly_earnings, columns=["symbol", "fiscal_quarter", "reported_date", "reported_EPS", "estimated_EPS", "surprise", "surprise_pct", "report_time"])

# Save DataFrames to CSV
annual_earnings_df.to_csv(annual_earnings_path, index=False)
quarterly_earnings_df.to_csv(quarterly_earnings_path, index=False)















