"""
================================================================
  Cloud Cost Intelligence - Data Analysis Script
  -----------------------------------------------
  This script performs end-to-end analysis of cloud billing data
  for a supply-chain company. It covers:
    1. Data Loading
    2. Data Cleaning & Preprocessing
    3. Exploratory Data Analysis (EDA)
    4. Data Visualization (charts saved to outputs/charts/)
    5. Cost Optimization Insights
    6. Excel Report Export

  Run:  python notebooks/analysis.py
  (From the project root directory)
================================================================
"""

import os
import sys
import warnings

import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # non-interactive backend (safe for scripts)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

warnings.filterwarnings("ignore")

# ── Paths ───────────────────────────────────────────────────
try:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    PROJECT_ROOT = os.path.dirname(os.getcwd())
DATA_PATH    = os.path.join(PROJECT_ROOT, "data", "cloud_billing_2024.csv")
CHARTS_DIR   = os.path.join(PROJECT_ROOT, "outputs", "charts")
REPORTS_DIR  = os.path.join(PROJECT_ROOT, "reports")

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ============================================================
# STEP 1 : DATA LOADING
# ============================================================
print("=" * 60)
print("  STEP 1 : Loading Data")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"\nDataset shape : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nFirst 5 rows:")
print(df.head().to_string(index=False))

print(f"\n--- Column Data Types ---")
print(df.dtypes)

print(f"\n--- Dataset Info ---")
print(df.info())

# ============================================================
# STEP 2 : DATA CLEANING & PREPROCESSING
# ============================================================
print("\n" + "=" * 60)
print("  STEP 2 : Data Cleaning & Preprocessing")
print("=" * 60)

# 2a. Check for duplicates
dup_count = df.duplicated().sum()
print(f"\n[1] Duplicate rows found : {dup_count}")
df.drop_duplicates(inplace=True)
print(f"    After removal         : {df.shape[0]} rows remain")

# 2b. Handle missing values
print(f"\n[2] Missing values per column:")
print(df.isnull().sum())

# Replace empty strings with NaN so pandas recognises them
df.replace("", pd.NA, inplace=True)

# Categorical columns -> fill with mode (most frequent value)
for col in ["Service_Type", "Region", "Cost_Category", "Department", "Resource_Tags"]:
    if df[col].isna().any():
        mode_val = df[col].mode()[0]
        df[col].fillna(mode_val, inplace=True)
        print(f"    Filled '{col}' missing values with mode: {mode_val}")

# Numerical columns -> fill with median
for col in ["Cost_USD", "Usage_Hours"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[col].isna().any():
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"    Filled '{col}' missing values with median: {median_val}")

# 2c. Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print(f"\n[3] Converted 'Date' column to datetime")

# 2d. Create derived columns
df["Month"]      = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b")       # Jan, Feb ...
df["Quarter"]    = df["Date"].dt.quarter
df["Day_of_Week"]= df["Date"].dt.day_name()

print(f"[4] Created columns: Month, Month_Name, Quarter, Day_of_Week")
print(f"\nCleaned dataset shape: {df.shape}")
print(df.head().to_string(index=False))

# ============================================================
# STEP 3 : EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
print("\n" + "=" * 60)
print("  STEP 3 : Exploratory Data Analysis")
print("=" * 60)

# 3a. Total Cloud Cost
total_cost = df["Cost_USD"].sum()
print(f"\n[1] Total Cloud Cost (2024) : ${total_cost:,.2f}")

# 3b. Cost by Service Type
cost_by_service = (
    df.groupby("Service_Type")["Cost_USD"]
    .sum()
    .sort_values(ascending=False)
)
print(f"\n[2] Cost by Service Type:")
print(cost_by_service.to_string())

# 3c. Cost by Month
cost_by_month = (
    df.groupby(["Month", "Month_Name"])["Cost_USD"]
    .sum()
    .reset_index()
    .sort_values("Month")
)
print(f"\n[3] Cost by Month:")
print(cost_by_month.to_string(index=False))

# 3d. Top 5 Costly Services
top5 = cost_by_service.head(5)
print(f"\n[4] Top 5 Most Costly Services:")
for rank, (svc, cost) in enumerate(top5.items(), 1):
    print(f"    {rank}. {svc:35s} ${cost:>12,.2f}")

# 3e. Region-wise Cost Distribution
cost_by_region = (
    df.groupby("Region")["Cost_USD"]
    .sum()
    .sort_values(ascending=False)
)
print(f"\n[5] Region-wise Cost Distribution:")
print(cost_by_region.to_string())

# 3f. Cost by Category
cost_by_category = (
    df.groupby("Cost_Category")["Cost_USD"]
    .sum()
    .sort_values(ascending=False)
)
print(f"\n[6] Cost by Pricing Category:")
print(cost_by_category.to_string())

# 3g. Department-wise Cost
cost_by_dept = (
    df.groupby("Department")["Cost_USD"]
    .sum()
    .sort_values(ascending=False)
)
print(f"\n[7] Department-wise Cost:")
print(cost_by_dept.to_string())

# ============================================================
# STEP 4 : DATA VISUALIZATION
# ============================================================
print("\n" + "=" * 60)
print("  STEP 4 : Data Visualization")
print("=" * 60)

# ── Chart Style ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0f1117",
    "axes.facecolor":   "#1a1d2e",
    "axes.edgecolor":   "#444",
    "axes.labelcolor":  "#ddd",
    "text.color":       "#ddd",
    "xtick.color":      "#aaa",
    "ytick.color":      "#aaa",
    "font.size":        11,
})

PALETTE = [
    "#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E",
    "#55EFC4", "#74B9FF", "#FF7675", "#A29BFE",
    "#E17055", "#00B894", "#D63031", "#0984E3",
    "#E84393", "#636E72", "#2D3436",
]

# ── 4a. Pie Chart – Cost by Service Type ────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    cost_by_service.values,
    labels=cost_by_service.index,
    autopct="%1.1f%%",
    colors=PALETTE[:len(cost_by_service)],
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="#0f1117", linewidth=1.5),
)
for t in autotexts:
    t.set_fontsize(8)
    t.set_color("white")
for t in texts:
    t.set_fontsize(8)
ax.set_title("Cost Distribution by Service Type", fontsize=16, fontweight="bold", pad=20)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "01_cost_by_service_pie.png"), dpi=150)
plt.close(fig)
print("[1] Saved: 01_cost_by_service_pie.png")

# ── 4b. Bar Chart – Monthly Cost ────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(
    cost_by_month["Month_Name"],
    cost_by_month["Cost_USD"],
    color=PALETTE[:len(cost_by_month)],
    edgecolor="#0f1117",
    linewidth=0.8,
    width=0.65,
)
# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, height + total_cost * 0.003,
        f"${height:,.0f}", ha="center", va="bottom", fontsize=8, color="#ddd",
    )
ax.set_title("Monthly Cloud Spending (2024)", fontsize=16, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Cost (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "02_monthly_cost_bar.png"), dpi=150)
plt.close(fig)
print("[2] Saved: 02_monthly_cost_bar.png")

# ── 4c. Horizontal Bar – Region-wise Cost ───────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
    cost_by_region.index,
    cost_by_region.values,
    color=PALETTE[:len(cost_by_region)],
    edgecolor="#0f1117",
    height=0.55,
)
for i, v in enumerate(cost_by_region.values):
    ax.text(v + total_cost * 0.003, i, f"${v:,.0f}", va="center", fontsize=10, color="#ddd")
ax.set_title("Region-wise Cloud Cost Distribution", fontsize=16, fontweight="bold")
ax.set_xlabel("Cost (USD)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.invert_yaxis()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "03_region_cost_bar.png"), dpi=150)
plt.close(fig)
print("[3] Saved: 03_region_cost_bar.png")

# ── 4d. Top 5 Services Bar ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
    top5.index[::-1],
    top5.values[::-1],
    color=["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#55EFC4"],
    edgecolor="#0f1117",
    height=0.55,
)
for i, v in enumerate(top5.values[::-1]):
    ax.text(v + total_cost * 0.002, i, f"${v:,.0f}", va="center", fontsize=10, color="#ddd")
ax.set_title("Top 5 Most Expensive Cloud Services", fontsize=16, fontweight="bold")
ax.set_xlabel("Cost (USD)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "04_top5_services.png"), dpi=150)
plt.close(fig)
print("[4] Saved: 04_top5_services.png")

# ── 4e. Department-wise Cost ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
    cost_by_dept.index[::-1],
    cost_by_dept.values[::-1],
    color=PALETTE[:len(cost_by_dept)],
    edgecolor="#0f1117",
    height=0.55,
)
for i, v in enumerate(cost_by_dept.values[::-1]):
    ax.text(v + total_cost * 0.002, i, f"${v:,.0f}", va="center", fontsize=10, color="#ddd")
ax.set_title("Department-wise Cloud Spending", fontsize=16, fontweight="bold")
ax.set_xlabel("Cost (USD)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "05_department_cost.png"), dpi=150)
plt.close(fig)
print("[5] Saved: 05_department_cost.png")

# ── 4f. Cost Category Distribution ──────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    cost_by_category.values,
    labels=cost_by_category.index,
    autopct="%1.1f%%",
    colors=["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E"],
    startangle=140,
    wedgeprops=dict(edgecolor="#0f1117", linewidth=1.5),
)
ax.set_title("Spending by Pricing Category", fontsize=16, fontweight="bold", pad=20)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "06_cost_category_pie.png"), dpi=150)
plt.close(fig)
print("[6] Saved: 06_cost_category_pie.png")

# ── 4g. Daily Cost Trend Line ───────────────────────────────
daily_cost = df.groupby("Date")["Cost_USD"].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(daily_cost["Date"], daily_cost["Cost_USD"], alpha=0.25, color="#6C5CE7")
ax.plot(daily_cost["Date"], daily_cost["Cost_USD"], color="#6C5CE7", linewidth=1.2)

# Add a rolling average line
rolling_avg = daily_cost["Cost_USD"].rolling(window=7).mean()
ax.plot(daily_cost["Date"], rolling_avg, color="#00CEC9", linewidth=2, label="7-day avg")

ax.set_title("Daily Cloud Spending Trend (2024)", fontsize=16, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Cost (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS_DIR, "07_daily_trend.png"), dpi=150)
plt.close(fig)
print("[7] Saved: 07_daily_trend.png")

print(f"\nAll charts saved to: {CHARTS_DIR}")

# ============================================================
# STEP 5 : COST OPTIMIZATION INSIGHTS
# ============================================================
print("\n" + "=" * 60)
print("  STEP 5 : Cost Optimization Insights")
print("=" * 60)

# Identify high-cost services (above average)
avg_service_cost = cost_by_service.mean()
high_cost = cost_by_service[cost_by_service > avg_service_cost]
print(f"\n--- High-Cost Services (above avg ${avg_service_cost:,.2f}) ---")
for svc, cost in high_cost.items():
    pct = (cost / total_cost) * 100
    print(f"  -> {svc:35s} ${cost:>12,.2f}  ({pct:.1f}% of total)")

# Detect daily anomalies (days where cost > mean + 2*std)
daily_mean = daily_cost["Cost_USD"].mean()
daily_std  = daily_cost["Cost_USD"].std()
threshold  = daily_mean + 2 * daily_std
anomalies  = daily_cost[daily_cost["Cost_USD"] > threshold]
print(f"\n--- Cost Spike Detection ---")
print(f"  Daily average : ${daily_mean:,.2f}")
print(f"  Spike threshold (mean + 2*std) : ${threshold:,.2f}")
print(f"  Days with cost spikes : {len(anomalies)}")
if len(anomalies) > 0:
    print(anomalies.to_string(index=False))

# On-Demand vs Reserved analysis
on_demand_cost = df[df["Cost_Category"] == "On-Demand"]["Cost_USD"].sum()
reserved_cost  = df[df["Cost_Category"] == "Reserved"]["Cost_USD"].sum()
potential_saving = on_demand_cost * 0.30       # Reserved can save ~30%
print(f"\n--- Reserved Instance Opportunity ---")
print(f"  On-Demand spending  : ${on_demand_cost:,.2f}")
print(f"  Reserved spending   : ${reserved_cost:,.2f}")
print(f"  Potential savings (30% of On-Demand) : ${potential_saving:,.2f}")

# Recommendations summary
print(f"\n--- Optimization Recommendations ---")
recommendations = [
    ("Reserved Instances",   f"Convert top On-Demand workloads to Reserved -> save ~${potential_saving:,.0f}"),
    ("Auto-scaling",         "Enable auto-scaling for EC2/EKS to match demand patterns"),
    ("Idle Resources",       "Audit resources with < 2 hrs/day usage for possible termination"),
    ("Storage Tiering",      "Move infrequently accessed S3 data to S3 Glacier (up to 68% cheaper)"),
    ("Right-sizing",         "Downsize over-provisioned instances based on actual CPU/memory usage"),
    ("Spot Instances",       "Use Spot for batch processing and non-critical supply-chain analytics"),
    ("Monitoring",           "Set up CloudWatch billing alerts at 80% and 100% of monthly budget"),
]
for i, (title, desc) in enumerate(recommendations, 1):
    print(f"  {i}. [{title}] {desc}")

# ============================================================
# STEP 6 : EXCEL EXPORT
# ============================================================
print("\n" + "=" * 60)
print("  STEP 6 : Excel / CSV Export")
print("=" * 60)

# 6a. Cleaned dataset
cleaned_path = os.path.join(REPORTS_DIR, "cleaned_billing_data.csv")
df.to_csv(cleaned_path, index=False)
print(f"[1] Cleaned dataset -> {cleaned_path}")

# 6b. Summary by Service
svc_summary = (
    df.groupby("Service_Type")
    .agg(
        Total_Cost=("Cost_USD", "sum"),
        Avg_Cost=("Cost_USD", "mean"),
        Max_Cost=("Cost_USD", "max"),
        Record_Count=("Cost_USD", "count"),
        Avg_Usage_Hours=("Usage_Hours", "mean"),
    )
    .round(2)
    .sort_values("Total_Cost", ascending=False)
)
svc_path = os.path.join(REPORTS_DIR, "summary_by_service.csv")
svc_summary.to_csv(svc_path)
print(f"[2] Service summary  -> {svc_path}")

# 6c. Summary by Month
month_summary = (
    df.groupby(["Month", "Month_Name"])
    .agg(
        Total_Cost=("Cost_USD", "sum"),
        Avg_Daily_Cost=("Cost_USD", "mean"),
        Max_Daily_Cost=("Cost_USD", "max"),
        Records=("Cost_USD", "count"),
    )
    .round(2)
    .reset_index()
    .sort_values("Month")
)
month_path = os.path.join(REPORTS_DIR, "summary_by_month.csv")
month_summary.to_csv(month_path, index=False)
print(f"[3] Month summary    -> {month_path}")

# 6d. Summary by Region
region_summary = (
    df.groupby("Region")
    .agg(Total_Cost=("Cost_USD", "sum"), Records=("Cost_USD", "count"))
    .round(2)
    .sort_values("Total_Cost", ascending=False)
)
region_path = os.path.join(REPORTS_DIR, "summary_by_region.csv")
region_summary.to_csv(region_path)
print(f"[4] Region summary   -> {region_path}")

# 6e. Optimization report (text)
report_path = os.path.join(REPORTS_DIR, "optimization_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("CLOUD COST OPTIMIZATION REPORT - 2024\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Total Cloud Spend: ${total_cost:,.2f}\n")
    f.write(f"Average Daily Spend: ${daily_mean:,.2f}\n")
    f.write(f"Cost Spike Days: {len(anomalies)}\n\n")
    f.write("HIGH-COST SERVICES\n" + "-" * 30 + "\n")
    for svc, cost in high_cost.items():
        f.write(f"  {svc}: ${cost:,.2f}\n")
    f.write("\nRECOMMENDATIONS\n" + "-" * 30 + "\n")
    for i, (title, desc) in enumerate(recommendations, 1):
        f.write(f"  {i}. [{title}] {desc}\n")
print(f"[5] Optimization report -> {report_path}")

# Try Excel export if openpyxl is available
try:
    excel_path = os.path.join(REPORTS_DIR, "cloud_cost_report.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        svc_summary.to_excel(writer, sheet_name="By Service")
        month_summary.to_excel(writer, sheet_name="By Month", index=False)
        region_summary.to_excel(writer, sheet_name="By Region")
    print(f"[6] Excel workbook   -> {excel_path}")
except ImportError:
    print("[6] Skipped Excel export (install openpyxl: pip install openpyxl)")

print("\n" + "=" * 60)
print("  ANALYSIS COMPLETE!")
print("=" * 60)
