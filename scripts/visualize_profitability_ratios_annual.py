from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

#===============================================================
#         VISUALIZE PROFITABILITY RATIOS (ANNUAL)
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
DATA_FILE = RESULTS_DIR / "profitability_ratios_annual.csv"
OUTPUT_FILE = FIGURES_DIR / "profitability_ratios_annual.png"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set context and style
sns.set_style("ticks")
sns.set_context("talk")

# Load data
df = pd.read_csv(DATA_FILE)

# Keep data for last 10 years and identify first and last year
df["fiscal_date"] = pd.to_datetime(df["fiscal_date"])
df["year"] = df["fiscal_date"].dt.year

latest_year = df["year"].max()
df = df[df["year"] >= latest_year-9]
earliest_year = df["year"].min()

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)

# Define a consistent color mapping to companies
palette = sns.color_palette("tab10")
companies = sorted(df["company_name"].unique())  # sort for consistency
color_map = dict(zip(companies, palette))

# Plot subplots
ratios = ["gross_margin", "net_margin", "return_on_assets", "return_on_equity"]
titles = ["Gross Margin (%)", "Net Margin (%)", "Return on Assets (%)", "Return on Equity (%)"]

for ax, ratio, title in zip(axes.flat, ratios, titles):
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
    ax.set_xlabel("Year")
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
plt.subplots_adjust(top=0.90, bottom=0.10)

# Set figure title
fig.suptitle("Profitability Ratios", fontsize=30)

# Create a single legend below the figure
handles, labels = axes[0, 0].get_legend_handles_labels() # grab legend and labels from first subplot

fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=len(companies),
    bbox_to_anchor=(0.5, -0.05),  # Adjusts position below the figure
    frameon=False,
    title="",
    fontsize=20 
)

fig.text(
    0.0, -0.13,
    "Note: "
    "This figure presents annual profitability ratios—gross margin, net margin, return on assets, "
    "and return on equity—for each company based on joined income statement and balance sheet data. "
    "Ratios are calculated using reported annual financials, with each fiscal year reflecting the "
    "figures from matching income statements and balance sheets. "
    "If an API key is provided, the data updates dynamically and includes the most recent 10 years. "
    f"The current dataset spans from {earliest_year} to {latest_year}.",
    wrap=True,
    horizontalalignment='left',
    fontsize=15
)


plt.show()

fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")








