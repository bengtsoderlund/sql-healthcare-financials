from pathlib import Path
import subprocess

#=======================
#         MAIN
#=======================


# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent
    
# Define the scripts directory
SCRIPTS_DIR = BASE_DIR / "scripts"

script_files = [
    "fetch_balance_sheets.py",
    "fetch_company_overviews.py",
    "fetch_earnings.py",
    "fetch_income_statements.py",
    "fetch_stock_prices.py",
    "load_to_db.py",
    "run_queries.py",
    "visualize_earnings_surprise_vs_price.py",
    "visualize_monthly_net_2pct_gain_counts.py",
    "visualize_post_earnings_drift.py",
    "visualize_profitability_ratios_annual.py",
    "visualize_stock_volatility.py",
    "visualize_valuation_multiples.py"
]

for script_file in script_files:
    script_path = SCRIPTS_DIR / script_file
    print(f"\nRunning {script_file}\n")
    try:
        subprocess.run(
            ["python", str(script_path)],
            check=True,
        )
        print(f"Finished {script_file}")
    except subprocess.CalledProcessError as e:
        print(f"Script {script_file} failed with error code: {e.returncode}")
        continue
