from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

#===============================================================
#         VISUALIZE STOCK VOLATILITY (LAST 6 MONTHS)
#===============================================================

# Set project root directory dynamically
try:
    BASE_DIR = Path(__file__).resolve().parent  # Normal execution
except NameError:
    BASE_DIR = Path().cwd()  # Interactive mode (Spyder)

if BASE_DIR.name == "scripts": # Move up one level
    BASE_DIR = BASE_DIR.parent
    
    
# Manage paths
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "figures"
DATA_FILE = RESULTS_DIR / "stock_volatility_last_6_months.csv"
OUTPUT_FILE = FIGURES_DIR / "stock_volatility_last_6_months.png"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set context and style
sns.set_style("darkgrid")
sns.set_context("notebook")


# Load data
df = pd.read_csv(DATA_FILE)

# Identify first and last date of data
df["month"] = pd.to_datetime(df["month"])
earliest_month = df["month"].min().strftime("%B %Y")
latest_month = df["month"].max().strftime("%B %Y")

plt.figure(figsize=(8, 5))

ax = sns.lineplot(
    data=df,
    x="month",
    y="avg_daily_return",
    hue="company_name",
    marker="o",
    markersize=8
)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_title("Average Daily Return by Month (%)", pad=15, fontsize=16)
ax.set_xlabel("")
ax.set_ylabel("Percent")
ax.legend(title="")

ax.figure.text(
    0.01, -0.08,
    "Note:\n"
    "This figure shows the average daily return for each stock, measured as the percentage change from open to close, over the most recent six full calendar months. "
    "If an API key is provided, the data updates dynamically. "
    f"The current dataset spans from {earliest_month} to {latest_month}.",
    wrap=True,
    horizontalalignment='left',
    fontsize=10
)


plt.show()

ax.figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")


