from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import seaborn as sns

#===============================================================
#         VISUALIZE CUMULATIVE 2% NET GAIN COUNTS
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
DATA_FILE = RESULTS_DIR / "monthly_net_2pct_gain_counts.csv"
OUTPUT_FILE = FIGURES_DIR / "monthly_net_2pct_gain_counts.png"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set context and style
sns.set_style("whitegrid")
sns.set_context("notebook")

# Load data
df = pd.read_csv(DATA_FILE)

# Generate cumulative gains
df["month"] = pd.to_datetime(df["month"])
df = df.sort_values(["symbol", "month"])
df["cumulative_gains"] = df.groupby("symbol")["nr_net_gains"].cumsum()

# Identify first and last date of data
earliest_date = df["month"].min().strftime("%B %Y")
latest_date = df["month"].max().strftime("%B %Y")

plt.figure(figsize=(9, 5))

ax = sns.lineplot(
    data=df,
    x="month",
    y="cumulative_gains",
    hue="company_name",
    marker="o",
    markersize=4
)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y %b"))

# Rotate x-tick labels 45 degrees
for label in ax.get_xticklabels():
    label.set_rotation(45)
    label.set_horizontalalignment('right')

ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=8)) # Reduce y-ticks and set to integers

ax.set_title("Cumulative Net Monthly Count of ±2% Days per Stock", pad=15)

ax.set_xlabel("")
ax.set_ylabel("Cumulative Net ±2% Days")

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="")

ax.figure.text(
    0.01, -0.2,
    "Note:\n"
    "This figure illustrates the cumulative monthly net count of days where a stock's open-to-close return exceeded +2% minus the number of days where it fell below −2%, based on the most recent 36 full calendar months. "
    "If an API key is provided, the data updates dynamically and includes the most recent 36 months. "
    f"The current dataset spans from {earliest_date} to {latest_date}.",
    wrap=True,
    horizontalalignment='left',
    fontsize=10
)

plt.show()

ax.figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")








