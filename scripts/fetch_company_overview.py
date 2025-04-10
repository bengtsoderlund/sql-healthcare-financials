from pathlib import Path
from dotenv import load_dotenv
import requests
import pandas as pd
import os
import json
import sys


#==================================================
#            FETCH COMPANY OVERVIEW
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent

# Manage output path
output_path = BASE_DIR / "data" / "company_overviews.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

# Load API key from environment variable
load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Stop execution if no API key is found
if not API_KEY or API_KEY == "your_actual_api_key_here":
    print("No valid API key found. Existing company overview data will be used instead.")
    sys.exit()
    
# Fetch data if API key exists
SYMBOLS = ["JNJ", "PFE", "UNH", "MDT"]
company_overviews = []

for SYMBOL in SYMBOLS:
    URL = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={SYMBOL}&apikey={API_KEY}"
    print(f"Fetching overview data for {SYMBOL}...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if response contains valid data
        if "Symbol" not in data:
            print(f"API request failed for {SYMBOL}. Existing company overview data will be used instead.")
            sys.exit()
            
        print(f"Overview data fetched successfully for {SYMBOL}!")
        
        # Process individual response: Ensure consistent data types
        processed_data = {
            "symbol": SYMBOL,
            "Name": data.get("Name", "Unknown"),
            "CIK": int(float(data.get("CIK") or 0)),
            "MarketCapitalization": int(float(data.get("MarketCapitalization") or 0)),
            "EBITDA": int(float(data.get("EBITDA") or 0)),
            "PERatio": float(data.get("PERatio") or 0),
            "PEGRatio": float(data.get("PEGRatio") or 0),
            "EPS": float(data.get("EPS") or 0),
            "ProfitMargin": float(data.get("ProfitMargin") or 0),
            "ReturnOnEquityTTM": float(data.get("ReturnOnEquityTTM") or 0),
            "RevenueTTM": int(data.get("RevenueTTM") or 0),
            "QuarterlyEarningsGrowthYOY": float(data.get("QuarterlyEarningsGrowthYOY") or 0),
            "QuarterlyRevenueGrowthYOY": float(data.get("QuarterlyRevenueGrowthYOY") or 0),
            "PriceToBookRatio": float(data.get("PriceToBookRatio") or 0),
            "DividendYield": float(data.get("DividendYield") or 0),
            "Beta": float(data.get("Beta") or 0)
        }
        
        company_overviews.append(processed_data)
      
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"API request error for {SYMBOL}: {e}. Existing company overview data will be used instead.")
        sys.exit()

# Create data frame
all_company_overviews = pd.DataFrame.from_records(company_overviews)

# Save DataFrame to CSV
all_company_overviews.to_csv(output_path, index=False)
