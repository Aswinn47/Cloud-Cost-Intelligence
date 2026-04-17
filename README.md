# ☁️ Cloud Cost Intelligence Platform for Supply Chain



![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)




![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat-square&logo=pandas)




![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)




![Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=flat-square)




![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)



# Cloud Cost Intelligence Platform for Supply Chain

A beginner-friendly, industry-standard project for analyzing and visualizing cloud billing data in a supply-chain context.

---

## What This Project Does

Cloud services (AWS, Azure, GCP) generate daily billing records.  This platform **loads**, **cleans**, **analyzes**, and **visualizes** that data so DevOps and finance teams can:

- Spot which services burn the most budget
- Detect unusual cost spikes before they snowball
- Find optimization opportunities (Reserved Instances, right-sizing, etc.)
- Track spending trends across regions, departments, and months

### Key Terms

| Term | Meaning |
|---|---|
| **Cloud Billing** | The detailed record of charges from your cloud provider for every service you use. |
| **Service Type** | A specific cloud product (e.g., EC2 for compute, S3 for storage, RDS for databases). |
| **Cost Optimization** | Techniques to reduce cloud spending without sacrificing performance. |
| **Data Analysis in DevOps** | Using data to make informed infrastructure and deployment decisions. |

---

## Project Structure

```
Cloud-Cost-Intelligence/
|
|-- data/
|   |-- cloud_billing_2024.csv        # Raw billing data (generated)
|
|-- notebooks/
|   |-- analysis.py                   # Full analysis script
|
|-- dashboard/
|   |-- app.py                        # Streamlit live dashboard
|
|-- outputs/
|   |-- charts/                       # Saved PNG charts
|
|-- reports/                          # CSV / Excel / text reports
|
|-- generate_data.py                  # Synthetic data generator
|-- requirements.txt                  # Python dependencies
|-- README.md                         # This file
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python generate_data.py
```

This creates `data/cloud_billing_2024.csv` with ~3,300 realistic billing records.

### 3. Run the Analysis

```bash
python notebooks/analysis.py
```

This will:
- Load and clean the data
- Perform exploratory data analysis
- Generate 7 charts in `outputs/charts/`
- Export reports to `reports/`

### 4. Launch the Live Dashboard

```bash
streamlit run dashboard/app.py
```

Your browser will open at `http://localhost:8501` with an interactive dashboard featuring:
- **Sidebar filters** — Month, Service Type, Region, Department, Date Range
- **KPI cards** — Total Cost, Avg Daily Spend, Top Service, Peak Month
- **Interactive charts** — Pie, Bar, Trend, Donut (Plotly)
- **Data table** with CSV download
- **Optimization insights** tab

---

## Dataset Columns

| Column | Description |
|---|---|
| `Date` | Billing date (YYYY-MM-DD) |
| `Service_Type` | Cloud service name |
| `Region` | AWS region code |
| `Cost_USD` | Daily cost in US dollars |
| `Cost_Category` | Pricing model (On-Demand, Reserved, Spot, Savings Plan) |
| `Department` | Supply-chain team that owns the resource |
| `Usage_Hours` | Hours the resource was active |
| `Resource_Tags` | Auto-generated tag for resource identification |

---

## Analysis Highlights

1. **Data Cleaning** — Removes duplicates, fills missing values (mode for categorical, median for numerical), converts dates.
2. **EDA** — Total cost, cost by service/month/region/department, top-5 services.
3. **Visualization** — 7 publication-quality charts with dark theme.
4. **Cost Optimization** — Identifies high-cost services, detects daily anomalies, calculates Reserved Instance savings potential.
5. **Export** — Cleaned CSV, summary reports, Excel workbook with multiple sheets.

---

## Technologies Used

- **Python 3.10+**
- **Pandas** — Data manipulation
- **Matplotlib** — Static charts
- **Plotly** — Interactive charts (dashboard)
- **Streamlit** — Live web dashboard
- **openpyxl** — Excel export

---

## License

This project is released for educational purposes. Feel free to modify and extend it.

