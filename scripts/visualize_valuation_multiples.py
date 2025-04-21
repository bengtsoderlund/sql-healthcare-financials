from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

#===============================================================
#               VISUALIZE VALUATION MULTIPLES
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
DATA_FILE = RESULTS_DIR / "valuation_multiples.csv"
OUTPUT_FILE = FIGURES_DIR / "valuation_multiples.png"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set context and style
sns.set_style("ticks")
sns.set_context("talk")

# Load data
df = pd.read_csv(DATA_FILE)

# Keep data for last 10 years and identify first and last year
df["price_date"] = pd.to_datetime(df["price_date"])
df["year"] = df["price_date"].dt.year

latest_year = df["year"].max()
df = df[df["year"] >= latest_year-9]
earliest_year = df["year"].min()

# Fix faulty value (incorrect net income)
idx = df[(df["symbol"] == "JNJ") & (df["year"] == 2018)].index
df.loc[idx, "PE"] = df.loc[idx, "PE"] / 10


# Create subplots
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Define a consistent color mapping to companies
palette = sns.color_palette("tab10")
companies = sorted(df["company_name"].unique())  # sort for consistency
color_map = dict(zip(companies, palette))

# Plot subplots
ratios = ["PE", "PS", "PB"]
titles = ["Price-to-Earnings Ratio (%)", "Price-to-Sales Ratio (%)", "Price-to-Book Ratio (%)"]

for ax, ratio, title in zip(axes, ratios, titles):
    sns.lineplot(
        data=df,
        x="year",
        y=ratio,
        hue="company_name",
        palette=color_map,
        marker="o",
        ax=ax
    )
    
    ax.legend_.remove() # Remove subplot legends (cannot use legend=False, since it's used to create legend)
    ax.set_title(title)
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=5, integer=True))
    plt.setp(ax.lines, markersize=8, linewidth=2)
    ax.yaxis.grid(True, linestyle="--", alpha=0.9)
    
# Adjust spines
for ax in axes.flat:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)

plt.tight_layout()
plt.subplots_adjust(top=0.80, bottom=0.20)

# Set figure title
fig.suptitle("Valuation Multiples", fontsize=20)

# Create a single legend below the figure
handles, labels = axes[0].get_legend_handles_labels() # grab legend and labels from first subplot

fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=len(companies),
    bbox_to_anchor=(0.5, -0.03),  # Adjusts position below the figure
    frameon=False,
    title="",
    fontsize=16
)

fig.text(
    0.0, -0.14,
    "Note: "
    "This figure presents annual valuation multiples—P/E, P/S, and P/B—for each company. "
    "Multiples are calculated using the first available closing price after each fiscal year-end, "
    "combined with fundamentals from matching annual income statements and balance sheets. "
    "This ensures consistent, year-by-year comparisons of relative market valuation."
    "If an API key is provided, the data updates dynamically and includes the most recent 10 years. "
    f"The current dataset spans from {earliest_year} to {latest_year}.",
    wrap=True,
    horizontalalignment='left',
    fontsize=14
)


plt.show()

fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
