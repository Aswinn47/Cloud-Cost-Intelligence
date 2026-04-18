"""
================================================================
  Cloud Cost Intelligence Dashboard  (Streamlit)
  -----------------------------------------------
  A fully interactive, production-style dashboard for
  visualizing and exploring cloud billing data.

  Run from project root:
      streamlit run dashboard/app.py

  Features:
    - Sidebar filters (Month, Service, Region, Date Range)
    - KPI metric cards
    - Interactive Plotly charts
    - Filterable data table
    - CSV download of filtered data
================================================================
"""

import os
# Auto-generate data if it doesn't exist (for cloud deployment)
if not os.path.exists("data/cloud_billing_2024.csv"):
    import generate_data  # runs the generator automatically
import sys

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cloud Cost Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paths ───────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH    = os.path.join(PROJECT_ROOT, "data", "cloud_billing_2024.csv")
REPORTS_DIR  = os.path.join(PROJECT_ROOT, "reports")


# ── Custom CSS for premium dark look ────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ───────────────────────────────────── */
:root {
    --bg-primary:   #0f1117;
    --bg-card:      #1a1d2e;
    --bg-card-alt:  #1e2235;
    --accent:       #6C5CE7;
    --accent-light: #A29BFE;
    --cyan:         #00CEC9;
    --pink:         #FD79A8;
    --yellow:       #FDCB6E;
    --green:        #55EFC4;
    --text-primary: #E8E8E8;
    --text-muted:   #8B8FA3;
    --border:       rgba(108, 92, 231, 0.15);
    --shadow:       0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ── Global ───────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #151929 50%, #0f1117 100%) !important;
}

/* ── Sidebar ──────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141728 0%, #0f1117 100%) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stDateInput label {
    color: var(--accent-light) !important;
    font-weight: 600;
    letter-spacing: 0.03em;
}

/* ── KPI Cards ────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-alt) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(108, 92, 231, 0.18);
}
div[data-testid="stMetric"] label {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}

/* ── Chart containers ─────────────────────────────────── */
div[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 12px;
    box-shadow: var(--shadow);
}

/* ── Dataframe ────────────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Headers ──────────────────────────────────────────── */
h1 {
    background: linear-gradient(90deg, var(--accent) 0%, var(--cyan) 50%, var(--pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}
h2, h3 {
    color: var(--accent-light) !important;
    font-weight: 600 !important;
}

/* ── Buttons / Downloads ──────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #5a4bd1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.8rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(108, 92, 231, 0.4) !important;
}

/* ── Tabs ─────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-light) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── Dividers ─────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data Loading ────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and preprocess the billing CSV."""
    df = pd.read_csv(DATA_PATH)

    # Basic cleaning (mirrors analysis.py logic)
    df.drop_duplicates(inplace=True)
    df.replace("", pd.NA, inplace=True)

    for col in ["Service_Type", "Region", "Cost_Category", "Department"]:
        if col in df.columns and df[col].isna().any():
            df[col].fillna(df[col].mode()[0], inplace=True)

    df["Cost_USD"] = pd.to_numeric(df["Cost_USD"], errors="coerce")
    df["Cost_USD"].fillna(df["Cost_USD"].median(), inplace=True)

    df["Usage_Hours"] = pd.to_numeric(df["Usage_Hours"], errors="coerce")
    df["Usage_Hours"].fillna(df["Usage_Hours"].median(), inplace=True)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"]      = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Quarter"]    = df["Date"].dt.quarter

    return df


df = load_data()

# ── Plotly Theme ────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#ccc"),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(
        bgcolor="#1a1d2e",
        font_color="#ddd",
        bordercolor="#6C5CE7",
    ),
)

COLOR_SEQUENCE = [
    "#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E",
    "#55EFC4", "#74B9FF", "#FF7675", "#A29BFE",
    "#E17055", "#00B894", "#D63031", "#0984E3",
    "#E84393", "#636E72", "#2D3436",
]


# ════════════════════════════════════════════════════════════
#   SIDEBAR  –  Filters
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Filters")
    st.markdown("---")

    # ── Date Range ──────────────────────────────────────────
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range",
    )

    # ── Month ───────────────────────────────────────────────
    all_months = sorted(df["Month"].unique())
    month_map  = {m: pd.Timestamp(2024, m, 1).strftime("%B") for m in all_months}
    selected_months = st.multiselect(
        "Month",
        options=all_months,
        default=all_months,
        format_func=lambda m: month_map[m],
        key="months",
    )

    # ── Service Type ────────────────────────────────────────
    all_services = sorted(df["Service_Type"].unique())
    selected_services = st.multiselect(
        "Service Type",
        options=all_services,
        default=all_services,
        key="services",
    )

    # ── Region ──────────────────────────────────────────────
    all_regions = sorted(df["Region"].unique())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
        key="regions",
    )

    # ── Department ──────────────────────────────────────────
    all_depts = sorted(df["Department"].unique())
    selected_depts = st.multiselect(
        "Department",
        options=all_depts,
        default=all_depts,
        key="departments",
    )

    st.markdown("---")
    st.caption("Cloud Cost Intelligence Platform v1.0")


# ── Apply Filters ───────────────────────────────────────────
filtered = df.copy()

# Date range filter (handle single-date edge case)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["Date"].dt.date >= start) &
        (filtered["Date"].dt.date <= end)
    ]

filtered = filtered[
    (filtered["Month"].isin(selected_months)) &
    (filtered["Service_Type"].isin(selected_services)) &
    (filtered["Region"].isin(selected_regions)) &
    (filtered["Department"].isin(selected_depts))
]

# ════════════════════════════════════════════════════════════
#   HEADER
# ════════════════════════════════════════════════════════════
st.markdown("# Cloud Cost Intelligence Dashboard")
st.caption(
    f"Analyzing **{len(filtered):,}** billing records "
    f"| Data period: **{df['Date'].min().strftime('%b %Y')}** to **{df['Date'].max().strftime('%b %Y')}**"
)
st.markdown("---")

# ════════════════════════════════════════════════════════════
#   KPI CARDS
# ════════════════════════════════════════════════════════════
total_cost       = filtered["Cost_USD"].sum()
avg_daily        = filtered.groupby("Date")["Cost_USD"].sum().mean() if len(filtered) else 0
most_expensive   = filtered.groupby("Service_Type")["Cost_USD"].sum().idxmax() if len(filtered) else "N/A"
peak_month_row   = filtered.groupby("Month_Name")["Cost_USD"].sum()
peak_month       = peak_month_row.idxmax() if len(peak_month_row) else "N/A"
total_records    = len(filtered)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Cost",         f"${total_cost:,.0f}")
k2.metric("Avg Daily Spend",    f"${avg_daily:,.0f}")
k3.metric("Top Service",        most_expensive)
k4.metric("Peak Month",         peak_month)
k5.metric("Records",            f"{total_records:,}")

st.markdown("")

# ════════════════════════════════════════════════════════════
#   CHARTS  –  Row 1  (Service Pie + Monthly Bar)
# ════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

# ── Pie : Cost by Service Type ──────────────────────────────
with col1:
    st.subheader("Cost by Service Type")
    svc_data = (
        filtered.groupby("Service_Type")["Cost_USD"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_pie = px.pie(
        svc_data,
        values="Cost_USD",
        names="Service_Type",
        color_discrete_sequence=COLOR_SEQUENCE,
        hole=0.45,
    )
    fig_pie.update_layout(**PLOTLY_LAYOUT, showlegend=True, legend=dict(font=dict(size=10)))
    fig_pie.update_traces(
        textinfo="percent+label",
        textfont_size=10,
        marker=dict(line=dict(color="#0f1117", width=1.5)),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Bar : Monthly Cost ──────────────────────────────────────
with col2:
    st.subheader("Monthly Cloud Spending")
    month_data = (
        filtered.groupby(["Month", "Month_Name"])["Cost_USD"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )
    fig_bar = px.bar(
        month_data,
        x="Month_Name",
        y="Cost_USD",
        color="Month_Name",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"Cost_USD": "Cost (USD)", "Month_Name": "Month"},
    )
    fig_bar.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=False,
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="$"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
    )
    fig_bar.update_traces(
        marker_line_color="#0f1117",
        marker_line_width=1,
        texttemplate="$%{y:,.0f}",
        textposition="outside",
        textfont_size=9,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════
#   CHARTS  –  Row 2  (Region + Department)
# ════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

# ── Region-wise Distribution ────────────────────────────────
with col3:
    st.subheader("Region-wise Cost")
    region_data = (
        filtered.groupby("Region")["Cost_USD"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    fig_region = px.bar(
        region_data,
        x="Cost_USD",
        y="Region",
        orientation="h",
        color="Region",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"Cost_USD": "Cost (USD)"},
    )
    fig_region.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="$"),
    )
    fig_region.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside",
        textfont_size=10,
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ── Department-wise Distribution ────────────────────────────
with col4:
    st.subheader("Department-wise Spending")
    dept_data = (
        filtered.groupby("Department")["Cost_USD"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    fig_dept = px.bar(
        dept_data,
        x="Cost_USD",
        y="Department",
        orientation="h",
        color="Department",
        color_discrete_sequence=COLOR_SEQUENCE[5:],
        labels={"Cost_USD": "Cost (USD)"},
    )
    fig_dept.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="$"),
    )
    fig_dept.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside",
        textfont_size=10,
    )
    st.plotly_chart(fig_dept, use_container_width=True)

# ════════════════════════════════════════════════════════════
#   CHARTS  –  Row 3  (Daily Trend + Cost Category)
# ════════════════════════════════════════════════════════════
col5, col6 = st.columns([2, 1])

# ── Daily Trend ─────────────────────────────────────────────
with col5:
    st.subheader("Daily Spending Trend")
    daily_data = (
        filtered.groupby("Date")["Cost_USD"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )
    daily_data["7d_avg"] = daily_data["Cost_USD"].rolling(window=7, min_periods=1).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily_data["Date"], y=daily_data["Cost_USD"],
        mode="lines",
        name="Daily Cost",
        line=dict(color="#6C5CE7", width=1),
        fill="tozeroy",
        fillcolor="rgba(108,92,231,0.15)",
    ))
    fig_trend.add_trace(go.Scatter(
        x=daily_data["Date"], y=daily_data["7d_avg"],
        mode="lines",
        name="7-day Average",
        line=dict(color="#00CEC9", width=2.5),
    ))
    fig_trend.update_layout(
        **PLOTLY_LAYOUT,
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="$"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ── Cost Category Donut ─────────────────────────────────────
with col6:
    st.subheader("Pricing Category")
    cat_data = (
        filtered.groupby("Cost_Category")["Cost_USD"]
        .sum()
        .reset_index()
    )
    fig_cat = px.pie(
        cat_data,
        values="Cost_USD",
        names="Cost_Category",
        color_discrete_sequence=["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E"],
        hole=0.5,
    )
    fig_cat.update_layout(**PLOTLY_LAYOUT, showlegend=True)
    fig_cat.update_traces(
        textinfo="percent+label",
        textfont_size=10,
        marker=dict(line=dict(color="#0f1117", width=1.5)),
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ════════════════════════════════════════════════════════════
#   TOP SERVICES TABLE
# ════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("Top Services Breakdown")

top_svc = (
    filtered.groupby("Service_Type")
    .agg(
        Total_Cost=("Cost_USD", "sum"),
        Avg_Cost=("Cost_USD", "mean"),
        Max_Cost=("Cost_USD", "max"),
        Records=("Cost_USD", "count"),
        Avg_Hours=("Usage_Hours", "mean"),
    )
    .round(2)
    .sort_values("Total_Cost", ascending=False)
    .reset_index()
)

# Format currency columns for display
display_svc = top_svc.copy()
for c in ["Total_Cost", "Avg_Cost", "Max_Cost"]:
    display_svc[c] = display_svc[c].apply(lambda v: f"${v:,.2f}")
display_svc["Avg_Hours"] = display_svc["Avg_Hours"].apply(lambda v: f"{v:.1f} hrs")

st.dataframe(display_svc, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════
#   DATA TABLE + DOWNLOAD
# ════════════════════════════════════════════════════════════
st.markdown("---")

tab1, tab2 = st.tabs(["Filtered Data", "Cost Optimization Insights"])

with tab1:
    st.subheader("Filtered Billing Records")
    st.dataframe(
        filtered[["Date", "Service_Type", "Region", "Cost_USD",
                  "Cost_Category", "Department", "Usage_Hours"]],
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    # Download button
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_cloud_billing.csv",
        mime="text/csv",
    )

with tab2:
    st.subheader("Cost Optimization Insights")

    if len(filtered) > 0:
        # High-cost services
        svc_costs = filtered.groupby("Service_Type")["Cost_USD"].sum()
        avg_svc   = svc_costs.mean()
        high_cost = svc_costs[svc_costs > avg_svc].sort_values(ascending=False)

        st.markdown("#### High-Cost Services")
        st.markdown(f"Services spending above average (${avg_svc:,.0f}):")

        for svc, cost in high_cost.items():
            pct = (cost / total_cost) * 100
            st.markdown(f"- **{svc}**: ${cost:,.0f} ({pct:.1f}% of filtered total)")

        st.markdown("---")

        # Recommendations
        st.markdown("#### Recommendations")

        rec_data = [
            ("Reserved Instances", "Convert frequent On-Demand workloads to 1-year or 3-year Reserved Instances for up to 40% savings.", "#6C5CE7"),
            ("Auto-scaling", "Enable auto-scaling for EC2 and EKS clusters to match actual demand patterns in logistics workflows.", "#00CEC9"),
            ("Idle Resource Audit", "Identify and terminate resources with consistently low usage hours (< 2 hrs/day).", "#FD79A8"),
            ("Storage Tiering", "Move infrequently accessed S3 data to S3 Glacier or Intelligent-Tiering (up to 68% cheaper).", "#FDCB6E"),
            ("Right-sizing", "Analyze CPU/memory utilization and downsize over-provisioned instances.", "#55EFC4"),
            ("Spot Instances", "Use Spot Instances for batch processing and non-critical supply-chain analytics jobs.", "#74B9FF"),
            ("Budget Alerts", "Set CloudWatch billing alarms at 80% and 100% of monthly budget targets.", "#FF7675"),
        ]

        for title, desc, color in rec_data:
            st.markdown(
                f'<div style="border-left:4px solid {color}; padding:10px 16px; '
                f'margin-bottom:10px; background:rgba(26,29,46,0.6); border-radius:0 8px 8px 0;">'
                f'<strong style="color:{color}">{title}</strong><br>'
                f'<span style="color:#aaa;font-size:0.9rem">{desc}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No data matches your current filters.")


# ── Footer ──────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#555; font-size:0.8rem; padding:10px 0">'
    'Cloud Cost Intelligence Platform v1.0  |  Built with Streamlit & Plotly'
    '</div>',
    unsafe_allow_html=True,
)
