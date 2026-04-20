<div align="center">

# CLOUD COST INTELLIGENCE PLATFORM
# FOR SUPPLY CHAIN

### Final Project Report

---

**Bachelor of Engineering / Technology**

**Department of Computer Science and Engineering**

**Academic Year 2025 – 2026**

---

| Field | Details |
|---|---|
| **Project Title** | Cloud Cost Intelligence Platform for Supply Chain |
| **Team Members** | *(Add your name(s) here)* |
| **Internal Guide** | *(Add guide name and designation)* |
| **External Guide** | *(Add if applicable)* |

---

*Institution Name*
*University Name*
*City, State – PIN Code*

</div>

---

<div align="center">

## CERTIFICATE

This is to certify that the project entitled **"Cloud Cost Intelligence Platform for Supply Chain"** is a bonafide work carried out by:

| Roll No. | Name |
|---|---|
| *(Roll No.)* | *(Your Name)* |

in partial fulfillment of the requirements for the award of the degree of **Bachelor of Engineering / Technology** in **Computer Science and Engineering** during the academic year **2025 – 2026**.

<br>

| | |
|---|---|
| **Internal Guide** | **Head of Department** |
| *(Name & Designation)* | *(Name & Designation)* |
| Signature: ____________ | Signature: ____________ |
| Date: ____________ | Date: ____________ |

<br>

**Principal**
*(Name & Designation)*
Signature: ____________

</div>

---

<div align="center">

## DECLARATION

</div>

We hereby declare that the project entitled **"Cloud Cost Intelligence Platform for Supply Chain"** submitted in partial fulfillment of the requirements for the degree of **Bachelor of Engineering / Technology** in **Computer Science and Engineering** is a record of original work done by us under the guidance of *(Internal Guide Name)*, *(Designation)*, Department of Computer Science and Engineering.

The results embodied in this project report have not been submitted to any other university or institution for the award of any degree or diploma.

| | |
|---|---|
| Place: ____________ | Name: ____________ |
| Date: ____________ | Signature: ____________ |

---

<div align="center">

## ACKNOWLEDGEMENT

</div>

We would like to express our sincere gratitude to ***(Principal Name)***, Principal of *(Institution Name)*, for providing the infrastructure and environment to carry out this project.

We extend our heartfelt thanks to ***(Vice Principal Name)***, Vice Principal, for the constant encouragement and support throughout the academic tenure.

We are deeply grateful to ***(HOD Name)***, Head of the Department of Computer Science and Engineering, for providing us with the opportunity and resources to undertake this project.

We are immensely thankful to our Internal Guide ***(Guide Name)***, *(Designation)*, for the invaluable guidance, constructive feedback, and continuous support during the course of this project.

*(If applicable)* We also sincerely thank our External Guide ***(External Guide Name)***, *(Designation, Organization)*, for their industry insights and mentorship.

Finally, we thank our family, friends, and all those who directly or indirectly helped us in the successful completion of this project.

---

<div align="center">

## TABLE OF CONTENTS

</div>

| No. | Section | 
|-----|---------|
| | Executive Summary |
| 1 | **Background** |
| 1.1 | Aim |
| 1.2 | Technologies |
| 1.3 | Hardware Architecture |
| 1.4 | Software Architecture |
| 2 | **System** |
| 2.1 | Requirements |
| 2.1.1 | Functional Requirements |
| 2.1.2 | User Requirements |
| 2.1.3 | Environmental Requirements |
| 2.2 | Design and Architecture |
| 2.3 | Implementation |
| 2.4 | Testing |
| 2.5 | Graphical User Interface (GUI) Layout |
| 2.6 | Customer Testing |
| 2.7 | Evaluation |
| 3 | Snapshots of the Project |
| 4 | Conclusions |
| 5 | Further Development or Research |
| 6 | References |
| 7 | Appendix |

---

<div align="center">

## EXECUTIVE SUMMARY

</div>

Cloud infrastructure spending has become one of the largest operational expenses for supply-chain organizations. Without proactive monitoring and data-driven insights, cloud costs can spiral beyond budget targets due to over-provisioned resources, idle instances, and missed commitment discounts.

The **Cloud Cost Intelligence Platform** addresses this challenge by providing an end-to-end, Python-based analytics solution that ingests daily cloud billing records, performs automated data cleaning, conducts exploratory data analysis, detects cost anomalies, and presents findings through an interactive web dashboard. The platform simulates a realistic supply-chain environment spanning 15 AWS services, 5 regions, 6 departments, and 4 pricing categories across a full calendar year (2024).

Key outcomes include the identification of **6 high-cost services** accounting for the majority of total spend ($396,097), detection of **14 cost-spike days** using statistical anomaly detection (mean + 2σ), and the quantification of **$30,571 in potential savings** through Reserved Instance conversion alone. The interactive Streamlit dashboard enables real-time filtering, KPI monitoring, and drill-down analysis, empowering FinOps teams to make data-driven optimization decisions.

---

## 1. BACKGROUND

### 1.1 Aim

The aim of this project is to design and develop a **Cloud Cost Intelligence Platform** that enables supply-chain organizations to:

- **Monitor** cloud spending across services, regions, and departments in real time.
- **Analyze** billing data to identify cost drivers, trends, and anomalies.
- **Optimize** cloud expenditure by recommending actionable cost-saving strategies such as Reserved Instances, right-sizing, auto-scaling, and storage tiering.
- **Report** insights through automated static charts, downloadable summaries, and an interactive live dashboard.

### 1.2 Technologies

| Category | Technology | Version | Purpose |
|---|---|---|---|
| Programming Language | Python | 3.10+ | Core application logic |
| Data Processing | Pandas | ≥ 1.5.0 | DataFrame operations, cleaning, aggregation |
| Data Processing | NumPy | (bundled) | Numerical computation, NaN handling |
| Static Visualization | Matplotlib | ≥ 3.6.0 | Publication-quality PNG charts |
| Statistical Viz | Seaborn | ≥ 0.12.0 | Enhanced statistical plots |
| Interactive Viz | Plotly | ≥ 5.18.0 | Browser-based interactive charts |
| Web Framework | Streamlit | ≥ 1.28.0 | Dashboard UI and hosting |
| Excel Export | openpyxl | ≥ 3.1.0 | Multi-sheet Excel workbook generation |
| Deployment | Streamlit Community Cloud | — | Free cloud hosting via GitHub |
| Version Control | Git / GitHub | — | Source code management |

### 1.3 Hardware Architecture

The platform is designed to run on standard consumer hardware with no specialized requirements:

| Component | Minimum Requirement | Recommended |
|---|---|---|
| Processor | Dual-core CPU (2.0 GHz) | Quad-core CPU (3.0 GHz+) |
| RAM | 4 GB | 8 GB or higher |
| Storage | 500 MB free space | 1 GB free space |
| Display | 1366 × 768 resolution | 1920 × 1080 (Full HD) |
| Network | Broadband internet | For Streamlit Cloud deployment |
| OS | Windows 10 / Ubuntu 20.04 / macOS 12+ | Any modern OS with Python 3.10+ |

**Cloud Deployment (Streamlit Community Cloud):**

| Resource | Allocation |
|---|---|
| RAM | 1 GB |
| CPU | Shared |
| Storage | Read-only (Git-mounted) |
| Availability | Sleeps after 7 days of inactivity; wakes on visit |

### 1.4 Software Architecture

The platform follows a **three-layered monolithic architecture**:

```
┌─────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                         │
│         Streamlit Dashboard (dashboard/app.py)          │
│  ┌──────────┬──────────┬───────────┬──────────────┐     │
│  │ Sidebar  │   KPI    │  Plotly   │  Data Tables │     │
│  │ Filters  │  Cards   │  Charts   │  & Download  │     │
│  └──────────┴──────────┴───────────┴──────────────┘     │
├─────────────────────────────────────────────────────────┤
│              BUSINESS LOGIC LAYER                       │
│        Analysis Engine (notebooks/analysis.py)          │
│  ┌──────────┬──────────┬───────────┬──────────────┐     │
│  │  Data    │   EDA    │  Anomaly  │    Cost      │     │
│  │ Cleaning │ Pipeline │ Detection │ Optimization │     │
│  └──────────┴──────────┴───────────┴──────────────┘     │
├─────────────────────────────────────────────────────────┤
│                  DATA LAYER                             │
│         Data Generator (generate_data.py)               │
│  ┌──────────┬──────────┬──────────────┐                 │
│  │ Synthetic│   CSV    │   Report     │                 │
│  │  Engine  │  Storage │   Export     │                 │
│  └──────────┴──────────┴──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

**Data Flow:**

```
generate_data.py ──(CSV)──► analysis.py ──(PNG/CSV/XLSX)──► outputs/ & reports/
       │
       └──(CSV / in-memory)──► dashboard/app.py ──(HTTP)──► User Browser
```

---

## 2. SYSTEM

### 2.1 Requirements

#### 2.1.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Generate synthetic cloud billing data with realistic patterns (seasonal spikes, anomalies) | High |
| FR-02 | Clean raw data: remove duplicates, impute missing values, coerce data types | High |
| FR-03 | Perform EDA: total cost, cost by service/month/region/department | High |
| FR-04 | Generate 7 static publication-quality charts (PNG) | Medium |
| FR-05 | Detect cost anomalies using statistical thresholds (mean + 2σ) | High |
| FR-06 | Produce optimization recommendations (Reserved Instances, right-sizing, etc.) | High |
| FR-07 | Export reports in CSV, Excel (multi-sheet), and text formats | Medium |
| FR-08 | Provide an interactive web dashboard with real-time filtering | High |
| FR-09 | Display KPI cards: Total Cost, Avg Daily Spend, Top Service, Peak Month, Records | High |
| FR-10 | Render 6 interactive Plotly charts (pie, bar, horizontal bar, trend line, donut) | High |
| FR-11 | Enable filtered data table with CSV download capability | Medium |
| FR-12 | Support in-memory data generation for read-only cloud environments | High |

#### 2.1.2 User Requirements

| ID | Requirement |
|---|---|
| UR-01 | Users must be able to filter data by date range, month, service type, region, and department |
| UR-02 | Users must view high-level KPI metrics at a glance |
| UR-03 | Users must be able to drill down into specific services or regions via interactive charts |
| UR-04 | Users must be able to download the filtered dataset as CSV |
| UR-05 | Users must access optimization recommendations and high-cost service alerts |
| UR-06 | Users must access the dashboard via any modern web browser without software installation |
| UR-07 | The dashboard must load within 3 seconds on standard broadband |

#### 2.1.3 Environmental Requirements

| Requirement | Specification |
|---|---|
| Python Runtime | Python 3.10 or higher |
| Package Manager | pip (with `requirements.txt`) |
| Browser | Chrome 90+, Firefox 88+, Edge 90+, Safari 14+ |
| Operating System | Windows 10+, macOS 12+, Ubuntu 20.04+ |
| Cloud Deployment | Streamlit Community Cloud (GitHub integration) |
| Network | Internet access for deployment; local mode works offline |

### 2.2 Design and Architecture

#### 2.2.1 Component Design

**Component 1 — Synthetic Data Generator (`generate_data.py`)**

Generates ~3,300 realistic billing records for Jan–Dec 2024 across 15 AWS services, 5 regions, 6 departments, and 4 pricing categories. Includes intentional data quality issues (15 duplicate rows, 20 missing values) to simulate real-world scenarios. Injects seasonal spikes for Nov–Dec (holiday logistics) and 3% random anomalies.

**Component 2 — Analysis Engine (`notebooks/analysis.py`)**

A 6-step sequential pipeline: Load → Clean → EDA → Visualize → Optimize → Export. Produces 7 Matplotlib charts, 4 CSV summaries, 1 multi-sheet Excel workbook, and 1 text-based optimization report. Anomaly detection uses the statistical method of mean + 2 standard deviations on daily spend.

**Component 3 — Interactive Dashboard (`dashboard/app.py`)**

A 656-line Streamlit application featuring custom CSS (dark theme with glassmorphism), 5 sidebar filter widgets, 5 KPI metric cards, 6 Plotly charts, a top-services breakdown table, a filterable data table with CSV download, and a cost optimization insights tab with 7 color-coded recommendations.

**Component 4 — Reporting Engine (embedded in analysis.py)**

Generates the following outputs:
- `cleaned_billing_data.csv` — Full cleaned dataset
- `summary_by_service.csv` — Aggregated cost per service
- `summary_by_month.csv` — Monthly spending breakdown
- `summary_by_region.csv` — Regional cost distribution
- `optimization_report.txt` — High-cost alerts and recommendations
- `cloud_cost_report.xlsx` — Multi-sheet Excel workbook

#### 2.2.2 Data Model

| Column | Data Type | Description |
|---|---|---|
| Date | DateTime | Billing date (YYYY-MM-DD) |
| Service_Type | String | AWS service (e.g., EC2, S3, RDS) |
| Region | String | AWS region code (e.g., us-east-1) |
| Cost_USD | Float | Daily cost in US dollars |
| Cost_Category | String | Pricing model (On-Demand, Reserved, Spot, Savings Plan) |
| Department | String | Supply-chain team (e.g., Logistics, Procurement) |
| Usage_Hours | Float | Hours the resource was active |
| Resource_Tags | String | Auto-generated resource identifier |

**Derived columns** (computed during cleaning): Month, Month_Name, Quarter, Day_of_Week.

#### 2.2.3 Process Flow

```
[User] ──► python generate_data.py ──► data/cloud_billing_2024.csv
                                              │
              ┌───────────────────────────────┤
              ▼                               ▼
   python notebooks/analysis.py     streamlit run dashboard/app.py
              │                               │
    ┌─────────┼─────────┐           ┌─────────┼──────────┐
    ▼         ▼         ▼           ▼         ▼          ▼
 Charts    Reports   Excel      Filters   Charts    KPI Cards
 (PNG)    (CSV/TXT)  (XLSX)    (Sidebar)  (Plotly)  (Metrics)
```

### 2.3 Implementation

#### 2.3.1 Project Structure

```
Cloud-Cost-Intelligence/
├── assets/                 # Screenshots for documentation
├── dashboard/
│   └── app.py              # Streamlit dashboard (656 lines)
├── data/
│   └── cloud_billing_2024.csv  # Generated dataset (~3,300 records)
├── docs/
│   ├── HLD.docx            # High-Level Design document
│   └── LLD.docx            # Low-Level Design document
├── notebooks/
│   ├── analysis.py         # Analysis pipeline (489 lines)
│   └── Cloud-Cost-Intelligence-Platform.ipynb
├── outputs/
│   └── charts/             # 7 auto-generated PNG charts
├── reports/                # CSV, Excel, and text reports
├── generate_data.py        # Synthetic data generator (182 lines)
├── requirements.txt        # Python dependencies
└── README.md               # GitHub documentation
```

#### 2.3.2 Module Implementation Details

**A. Data Generation Module**

The `generate_data.py` script uses Python's `random` module (seeded with 42 for reproducibility) to create billing records. Key implementation features:

- **Seasonal Simulation:** Nov–Dec costs are multiplied by a factor of 1.15–1.50 to simulate holiday logistics surges.
- **Anomaly Injection:** 3% of records receive a 2x–4x cost multiplier to simulate misconfigured or idle resources.
- **Data Quality Issues:** 15 duplicate rows and 20 missing values are intentionally injected for the cleaning pipeline to handle.
- **Resource Tagging:** Tags are auto-generated using the pattern `{department}-{service}` for resource identification.

**B. Analysis Pipeline**

The `analysis.py` script implements a 6-step pipeline:

| Step | Operation | Output |
|---|---|---|
| Step 1 | Load CSV with `pd.read_csv()` | DataFrame in memory |
| Step 2 | Remove duplicates, fill missing values (mode for categorical, median for numerical), convert date types | Cleaned DataFrame |
| Step 3 | Compute aggregations: total cost, cost by service/month/region/department, top-5 services | Console output |
| Step 4 | Generate 7 Matplotlib charts with dark theme styling | 7 PNG files in `outputs/charts/` |
| Step 5 | Detect anomalies (mean + 2σ), identify high-cost services, calculate RI savings potential | Console output |
| Step 6 | Export cleaned CSV, summary CSVs, optimization report, and multi-sheet Excel workbook | 6 files in `reports/` |

**C. Dashboard Application**

The `dashboard/app.py` Streamlit application features:

- **Custom CSS:** 130+ lines of custom styling with CSS variables for a premium dark theme, gradient backgrounds, glassmorphism cards, hover animations, and Google Fonts (Inter).
- **Data Loading:** `@st.cache_data` decorator ensures data is loaded only once; supports both CSV file reading and in-memory generation for cloud deployment.
- **Sidebar Filters:** 5 interactive widgets (date range, month, service type, region, department) with multi-select capability.
- **KPI Cards:** 5 metric cards with hover effects showing Total Cost, Avg Daily Spend, Top Service, Peak Month, and Record Count.
- **Charts:** 6 Plotly visualizations — service pie chart, monthly bar chart, region horizontal bar, department horizontal bar, daily trend line with 7-day moving average, and pricing category donut chart.
- **Data Tables:** Top services breakdown table with formatted currency, and a filterable billing records table with CSV download.
- **Optimization Tab:** Identifies above-average cost services and displays 7 color-coded recommendations.

### 2.4 Testing

#### 2.4.1 Testing Strategy

| Test Type | Scope | Method |
|---|---|---|
| Unit Testing | Data generation functions | Verified output row count, column names, data types, and value ranges |
| Data Quality Testing | Cleaning pipeline | Confirmed duplicate removal, missing value imputation, and type coercion |
| Integration Testing | End-to-end pipeline | Ran `generate_data.py` → `analysis.py` → `dashboard/app.py` sequentially |
| Visual Testing | Charts and dashboard | Manual inspection of all 7 static charts and 6 interactive charts |
| Cross-Browser Testing | Dashboard UI | Tested on Chrome, Firefox, and Edge |
| Cloud Deployment Testing | Streamlit Cloud | Verified in-memory data generation on read-only filesystem |

#### 2.4.2 Test Results

| Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|
| Generate ~3,300 billing records | CSV with 8 columns, ~3,300 rows | 3,316 rows generated | ✅ Pass |
| Remove duplicate rows | 15 duplicates removed | 15 duplicates removed | ✅ Pass |
| Fill missing Service_Type values | No NaN in column after cleaning | All values filled with mode | ✅ Pass |
| Fill missing Cost_USD values | No NaN, median-imputed | All values filled with median | ✅ Pass |
| Detect cost anomalies | Identify spike days (mean + 2σ) | 14 spike days detected | ✅ Pass |
| Generate 7 static charts | 7 PNG files in outputs/charts/ | All 7 files created | ✅ Pass |
| Dashboard loads without error | No exceptions on startup | Dashboard renders successfully | ✅ Pass |
| Sidebar filters work correctly | Data updates on filter change | All 5 filters functional | ✅ Pass |
| CSV download works | File downloads on click | CSV file downloaded correctly | ✅ Pass |
| Cloud deployment (Streamlit Cloud) | App accessible via public URL | App runs with in-memory data | ✅ Pass |

### 2.5 Graphical User Interface (GUI) Layout

The dashboard follows a **top-down, responsive layout** designed for wide screens:

```
┌──────────────────────────────────────────────────────────────┐
│  SIDEBAR              │           MAIN CONTENT AREA          │
│  ┌──────────────┐     │  ┌────────────────────────────────┐  │
│  │ Date Range   │     │  │  HEADER: Title + Record Count  │  │
│  │ Filter       │     │  └────────────────────────────────┘  │
│  ├──────────────┤     │  ┌─────┬─────┬─────┬─────┬─────┐    │
│  │ Month        │     │  │ KPI │ KPI │ KPI │ KPI │ KPI │    │
│  │ Filter       │     │  │  1  │  2  │  3  │  4  │  5  │    │
│  ├──────────────┤     │  └─────┴─────┴─────┴─────┴─────┘    │
│  │ Service Type │     │  ┌──────────────┬──────────────┐     │
│  │ Filter       │     │  │  Pie Chart   │  Bar Chart   │     │
│  ├──────────────┤     │  │  (Service)   │  (Monthly)   │     │
│  │ Region       │     │  └──────────────┴──────────────┘     │
│  │ Filter       │     │  ┌──────────────┬──────────────┐     │
│  ├──────────────┤     │  │  H-Bar Chart │  H-Bar Chart │     │
│  │ Department   │     │  │  (Region)    │  (Dept)      │     │
│  │ Filter       │     │  └──────────────┴──────────────┘     │
│  └──────────────┘     │  ┌───────────────────┬─────────┐     │
│                       │  │  Trend Line       │  Donut  │     │
│  v1.0 Caption         │  │  (Daily + 7d avg) │  Chart  │     │
│                       │  └───────────────────┴─────────┘     │
│                       │  ┌────────────────────────────────┐  │
│                       │  │  Top Services Breakdown Table  │  │
│                       │  └────────────────────────────────┘  │
│                       │  ┌─────────────┬──────────────────┐  │
│                       │  │ Tab: Data   │ Tab: Optimize    │  │
│                       │  │ + Download  │ + Recommendations│  │
│                       │  └─────────────┴──────────────────┘  │
│                       │  ┌────────────────────────────────┐  │
│                       │  │        FOOTER v1.0             │  │
│                       │  └────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**Design Features:**
- Dark gradient background (`#0f1117` → `#151929`)
- Glassmorphism KPI cards with hover lift animation
- Custom Google Font (Inter) with 300–800 weight range
- Color palette: Purple (#6C5CE7), Cyan (#00CEC9), Pink (#FD79A8), Yellow (#FDCB6E), Green (#55EFC4)
- Responsive layout adapting to screen width via Streamlit columns

### 2.6 Customer Testing

| Scenario | Steps | Expected Outcome | Result |
|---|---|---|---|
| First-time setup | Clone repo → pip install → generate data → run dashboard | Dashboard opens at localhost:8501 | ✅ Pass |
| Filter by single service | Select only "EC2 (Compute)" in sidebar | All charts and KPIs update to show EC2 data only | ✅ Pass |
| Filter by date range | Set range to Jan–Mar 2024 | Only Q1 data visible | ✅ Pass |
| Download filtered data | Apply filters → click "Download Filtered Data as CSV" | CSV file downloads with filtered records | ✅ Pass |
| View optimization insights | Click "Cost Optimization Insights" tab | 7 recommendations displayed with color coding | ✅ Pass |
| Access cloud-hosted version | Visit Streamlit Cloud URL | Dashboard loads with auto-generated data | ✅ Pass |
| Run analysis pipeline | Execute `python notebooks/analysis.py` | 7 charts + 6 reports created | ✅ Pass |

### 2.7 Evaluation

#### Performance Metrics

| Metric | Measured Value |
|---|---|
| Data generation time | < 1 second (3,316 records) |
| Analysis pipeline execution | ~5 seconds (all 6 steps) |
| Dashboard initial load | < 2 seconds (cached) |
| Filter response time | < 500 ms |
| Memory usage (dashboard) | ~100 MB |
| Dataset size on disk | 328 KB (CSV) |

#### Analytical Results

| Insight | Value |
|---|---|
| Total cloud spend (2024) | $396,097.19 |
| Average daily spend | $1,082.23 |
| Top cost service | EKS (Kubernetes) — $65,863 |
| Cost spike days detected | 14 out of 366 |
| Potential RI savings | $30,571 (30% of On-Demand) |
| High-cost services (above average) | 6 services identified |

---

## 3. SNAPSHOTS OF THE PROJECT

*(Insert screenshots of your project here. Below are the recommended screenshots with descriptions:)*

**Snapshot 1: Dashboard Overview**
> Shows the main dashboard with KPI cards, service pie chart, and monthly bar chart with all filters set to default.

*(Insert screenshot: `assets/dashboard1.png`)*

**Snapshot 2: Cost Optimization Insights**
> Shows the optimization tab with high-cost service alerts and 7 color-coded recommendations.

*(Insert screenshot: `assets/optimization.png`)*

**Snapshot 3: Static Analysis Charts**
> Sample output from the analysis pipeline showing cost-by-service pie chart and daily trend line.

*(Insert screenshots from: `outputs/charts/01_cost_by_service_pie.png` and `outputs/charts/07_daily_trend.png`)*

**Snapshot 4: Sidebar Filters in Action**
> Shows the dashboard with specific filters applied (e.g., single service, single region), demonstrating real-time data update.

**Snapshot 5: Data Table with CSV Download**
> Shows the filterable billing records table and the download button.

**Snapshot 6: Generated Reports**
> Shows the contents of the `reports/` folder with all exported files.

---

## 4. CONCLUSIONS

The **Cloud Cost Intelligence Platform for Supply Chain** successfully meets all defined project objectives:

1. **Data Generation:** A robust synthetic data generator creates realistic billing scenarios with seasonal trends, cost anomalies, and intentional data quality issues for pipeline testing.

2. **Data Cleaning:** The automated cleaning pipeline handles duplicates (15 removed), missing values (20 imputed via mode/median), and type coercion reliably across both local and cloud environments.

3. **Exploratory Analysis:** Comprehensive EDA reveals that EKS, SageMaker, and EC2 are the top cost drivers, November and December show seasonal spending surges, and spending is distributed unevenly across regions and departments.

4. **Anomaly Detection:** The statistical threshold method (mean + 2σ) effectively identifies 14 cost-spike days that warrant investigation, providing early warning capability for FinOps teams.

5. **Interactive Dashboard:** The Streamlit-based dashboard delivers a premium, real-time filtering experience with 5 KPI cards, 6 interactive Plotly charts, and drill-down capability — all accessible via any modern web browser.

6. **Optimization Insights:** The platform quantifies potential savings ($30,571 via RI conversion) and provides 7 actionable recommendations spanning Reserved Instances, auto-scaling, idle resource audits, storage tiering, right-sizing, Spot Instances, and budget alerting.

7. **Cloud Deployment:** Successfully deployed to Streamlit Community Cloud with in-memory data generation handling the read-only filesystem constraint.

The platform demonstrates that meaningful cloud cost intelligence can be achieved using open-source Python tools without requiring expensive FinOps SaaS subscriptions.

---

## 5. FURTHER DEVELOPMENT OR RESEARCH

| Area | Description |
|---|---|
| **Real Data Integration** | Replace synthetic data with live feeds from AWS Cost Explorer API, Azure Cost Management, or GCP Billing Export for production use. |
| **Multi-Cloud Support** | Extend the data model to normalize billing records across AWS, Azure, and GCP into a unified schema. |
| **Machine Learning Forecasting** | Implement time-series forecasting (ARIMA, Prophet, or LSTM) to predict future cloud spending and enable proactive budgeting. |
| **Automated Alerts** | Add Slack, email, or SMS notifications when daily spend exceeds defined thresholds or anomalies are detected. |
| **Database Backend** | Migrate from CSV to PostgreSQL or a cloud data warehouse (Redshift, BigQuery) for handling larger datasets (1M+ records). |
| **Role-Based Access Control** | Implement authentication and department-level authorization so each team sees only their own spending data. |
| **Tagging Compliance** | Add a module to detect untagged or improperly tagged resources, which is a major cause of unattributed cloud spend. |
| **Kubernetes Cost Allocation** | Integrate with Kubernetes cost tools (e.g., Kubecost) for granular container-level cost attribution. |
| **CI/CD Integration** | Embed cost impact estimation into the CI/CD pipeline to flag infrastructure changes that may increase cloud spend. |

---

## 6. REFERENCES

| # | Reference |
|---|---|
| 1 | Python Software Foundation. "Python 3.10 Documentation." https://docs.python.org/3.10/ |
| 2 | Pandas Development Team. "Pandas User Guide." https://pandas.pydata.org/docs/user_guide/ |
| 3 | Streamlit Inc. "Streamlit Documentation." https://docs.streamlit.io |
| 4 | Plotly Technologies. "Plotly Python Open Source Graphing Library." https://plotly.com/python/ |
| 5 | Hunter, J.D. "Matplotlib: A 2D Graphics Environment." Computing in Science & Engineering, 2007. https://matplotlib.org |
| 6 | Amazon Web Services. "AWS Cost Management." https://aws.amazon.com/aws-cost-management/ |
| 7 | FinOps Foundation. "FinOps Framework." https://www.finops.org/framework/ |
| 8 | Streamlit Inc. "Streamlit Caching." https://docs.streamlit.io/develop/concepts/architecture/caching |
| 9 | McKinney, W. "Python for Data Analysis." O'Reilly Media, 2022. |
| 10 | openpyxl Documentation. https://openpyxl.readthedocs.io/ |

---

## 7. APPENDIX

### Appendix A: Requirements File (`requirements.txt`)

```
pandas>=1.5.0
matplotlib>=3.6.0
seaborn>=0.12.0
streamlit>=1.28.0
plotly>=5.18.0
openpyxl>=3.1.0
```

### Appendix B: Sample Data Record

```csv
Date,Service_Type,Region,Cost_USD,Cost_Category,Department,Usage_Hours,Resource_Tags
2024-03-15,EC2 (Compute),us-east-1,287.45,On-Demand,Logistics,18.3,logistics-ec2
2024-07-22,S3 (Storage),eu-west-1,54.12,Reserved,Data Engineering,24.0,data-engineering-s3
2024-11-08,EKS (Kubernetes),ap-south-1,612.87,On-Demand,Platform / DevOps,22.1,platform-/-devops-eks
```

### Appendix C: Optimization Report Summary

```
Total Cloud Spend:   $396,097.19
Average Daily Spend: $1,082.23
Cost Spike Days:     14

HIGH-COST SERVICES:
  EKS (Kubernetes):          $65,863.49
  SageMaker (ML):            $59,892.45
  EC2 (Compute):             $56,636.72
  RDS (Database):            $51,603.44
  Redshift (Data Warehouse): $46,708.72
  DynamoDB (NoSQL):          $28,461.26
```

### Appendix D: Setup Commands

```bash
# Clone the repository
git clone https://github.com/aswinn47/Cloud-Cost-Intelligence.git
cd Cloud-Cost-Intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_data.py

# Run analysis pipeline
python notebooks/analysis.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

<div align="center">

**— End of Final Project Report —**

**Cloud Cost Intelligence Platform for Supply Chain**

**Version 1.0 | April 2026**

</div>
