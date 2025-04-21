from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#====================================================================
#           VISUALIZE POST EARNINGS DRIFT
#====================================================================


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
DATA_FILE = RESULTS_DIR / "post_earnings_drift.csv"
OUTPUT_FILE = FIGURES_DIR / "post_earnings_drift.png"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set context and style
sns.set_style("white")
sns.set_context("notebook")

# Load data
df = pd.read_csv(DATA_FILE)

# Identify first and last date of data
df["fiscal_quarter"] = pd.to_datetime(df["fiscal_quarter"])
earliest_date = df["fiscal_quarter"].min()
latest_date = df["fiscal_quarter"].max()


# Remove outliers (keep 5th to 95th percentile)
for col in ["surprise_pct","post_earnings_drift_pct"]:
    lower = df[col].quantile(0.05)
    upper = df[col].quantile(0.95)
    df = df[(df[col] >= lower) & (df[col] <= upper)]

g  = sns.lmplot(
    data=df,
    x="surprise_pct",
    y="post_earnings_drift_pct",
    col="name",
    col_wrap=2,
    facet_kws={"sharex": False, "sharey": True},
    height=4,
    aspect=1
    )

g.fig.suptitle("Relationship Between Earnings Surprise and Stock Return 6–20 Days After Earnings", y=1.05)
g.set_axis_labels("Earnings Surprise (%)", "6–20 Day Post-Earnings Stock Return (%)")
g.set_titles("{col_name}")


plt.figtext(
    0.01, -0.08,
    "Note:\n"
    "This figure illustrates the relationship between the earnings surprise (%) and the stock return from trading day 6 to day 20 following the earnings report. "
    "If an API key is provided, the data updates dynamically and includes the most recent 20 quarters. "
    f"The current dataset spans from Q{earliest_date.quarter} {earliest_date.year} to Q{latest_date.quarter} {latest_date.year}. "
    "To minimize the impact of extreme values, data is trimmed to the 5th–95th percentile.",
    wrap=True,
    horizontalalignment='left',
    fontsize=10
)

plt.show()

g.fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
