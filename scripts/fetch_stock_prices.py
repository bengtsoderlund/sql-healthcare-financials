from pathlib import Path
from dotenv import load_dotenv
import requests
import pandas as pd
import os
import json
import sys


#==================================================
#              FETCH STOCK PRICES
#==================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent

# Manage output path
output_path = BASE_DIR / "data" / "stock_prices.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

# Load API key from environment variable
load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Stop execution if no API key is found
if not API_KEY or API_KEY == "your_actual_api_key_here":
    print("No valid API key found. Existing stock price data will be used instead.")
    sys.exit()

# Fetch data if API key exists
SYMBOLS = ["JNJ", "PFE", "UNH", "MDT"]
all_stock_prices = []

for SYMBOL in SYMBOLS:
    URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize=full&apikey={API_KEY}"
    print(f"Fetching stock prices for {SYMBOL}...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if response contains valid data
        if "Time Series (Daily)" not in data:
            print(f"API request failed for {SYMBOL}. Existing stock price data will be used instead.")
            sys.exit()
            
        print(f"Stock prices fetched successfully for {SYMBOL}!")
        
        # Extract stock prices
        stock_prices = []
        for date, values in data["Time Series (Daily)"].items():
            stock_prices.append([
                SYMBOL,
                date,
                float(values["1. open"]),
                float(values["2. high"]),
                float(values["3. low"]),
                float(values["4. close"]),
                float(values["5. volume"]),
                ])
            
        all_stock_prices.extend(stock_prices)
        
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"API request error for {SYMBOL}: {e}. Existing stock price data will be used instead.")
        sys.exit()

# Convert to DataFrame
df = pd.DataFrame(all_stock_prices, columns=["symbol", "date", "open", "high", "low", "close", "volume"])

# Save DataFrame to CSV
df.to_csv(output_path, index=False)




















