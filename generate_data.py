"""
============================================================
  generate_data.py  –  Synthetic Cloud Billing Data Generator
============================================================

This script creates a realistic cloud billing CSV dataset
that simulates 12 months of cloud spending across various
services, regions, and cost categories for a supply-chain
company.

Run once:  python generate_data.py
Output  :  data/cloud_billing_2024.csv
"""

import csv
import random
import os
from datetime import datetime, timedelta

# ── Seed for reproducibility ────────────────────────────────
random.seed(42)

# ── Configuration ───────────────────────────────────────────

# Cloud services commonly used in supply-chain workloads
SERVICES = [
    "EC2 (Compute)",
    "S3 (Storage)",
    "RDS (Database)",
    "Lambda (Serverless)",
    "CloudFront (CDN)",
    "EKS (Kubernetes)",
    "SageMaker (ML)",
    "Redshift (Data Warehouse)",
    "DynamoDB (NoSQL)",
    "ElastiCache (Caching)",
    "SNS (Notifications)",
    "SQS (Queue)",
    "API Gateway",
    "CloudWatch (Monitoring)",
    "Route 53 (DNS)",
]

# Regions where supply-chain workloads typically run
REGIONS = [
    "us-east-1",
    "us-west-2",
    "eu-west-1",
    "ap-south-1",
    "ap-southeast-1",
]

# Cost category labels for deeper analysis
COST_CATEGORIES = ["On-Demand", "Reserved", "Spot", "Savings Plan"]

# Supply-chain departments / teams that own cloud resources
DEPARTMENTS = [
    "Logistics",
    "Warehouse Ops",
    "Procurement",
    "Fleet Management",
    "Data Engineering",
    "Platform / DevOps",
]

# Base cost ranges per service (min, max USD per day)
SERVICE_COST_RANGES = {
    "EC2 (Compute)":             (80, 450),
    "S3 (Storage)":              (20, 120),
    "RDS (Database)":            (60, 350),
    "Lambda (Serverless)":       (5, 80),
    "CloudFront (CDN)":          (15, 90),
    "EKS (Kubernetes)":          (100, 500),
    "SageMaker (ML)":            (50, 400),
    "Redshift (Data Warehouse)": (70, 300),
    "DynamoDB (NoSQL)":          (30, 180),
    "ElastiCache (Caching)":     (25, 150),
    "SNS (Notifications)":       (2, 20),
    "SQS (Queue)":               (3, 25),
    "API Gateway":               (10, 60),
    "CloudWatch (Monitoring)":   (8, 50),
    "Route 53 (DNS)":            (1, 10),
}


def generate_billing_data(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    records_per_day: int = 8,
) -> list[dict]:
    """
    Generate synthetic daily cloud billing records.

    Parameters
    ----------
    start_date : str   – First date (inclusive), ISO format.
    end_date   : str   – Last  date (inclusive), ISO format.
    records_per_day : int – Approximate records generated per day.

    Returns
    -------
    list[dict]  – Each dict represents one billing row.
    """
    rows = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end     = datetime.strptime(end_date,   "%Y-%m-%d")

    while current <= end:
        # Vary the number of records per day slightly
        n_records = random.randint(records_per_day - 2, records_per_day + 4)

        for _ in range(n_records):
            service  = random.choice(SERVICES)
            region   = random.choice(REGIONS)
            category = random.choice(COST_CATEGORIES)
            dept     = random.choice(DEPARTMENTS)

            lo, hi = SERVICE_COST_RANGES[service]
            base_cost = round(random.uniform(lo, hi), 2)

            # Simulate seasonal spikes (holiday logistics in Nov-Dec)
            month = current.month
            if month in (11, 12):
                base_cost *= random.uniform(1.15, 1.50)

            # Simulate occasional cost spikes (idle / mis-configured resources)
            if random.random() < 0.03:          # 3 % chance of anomaly
                base_cost *= random.uniform(2.0, 4.0)

            usage_hours = round(random.uniform(1, 24), 1)

            rows.append({
                "Date":           current.strftime("%Y-%m-%d"),
                "Service_Type":   service,
                "Region":         region,
                "Cost_USD":       round(base_cost, 2),
                "Cost_Category":  category,
                "Department":     dept,
                "Usage_Hours":    usage_hours,
                "Resource_Tags":  f"{dept.lower().replace(' ', '-')}-{service.split('(')[0].strip().lower()}",
            })

        current += timedelta(days=1)

    # Inject a handful of intentional quality issues for the cleaning step
    # 1. Duplicate rows
    for _ in range(15):
        rows.append(random.choice(rows).copy())

    # 2. Missing values
    for _ in range(20):
        idx = random.randint(0, len(rows) - 1)
        field = random.choice(["Service_Type", "Region", "Cost_USD"])
        rows[idx][field] = ""

    random.shuffle(rows)
    return rows


def save_csv(rows: list[dict], path: str) -> None:
    """Write rows to a CSV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = [
        "Date", "Service_Type", "Region", "Cost_USD",
        "Cost_Category", "Department", "Usage_Hours", "Resource_Tags",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] Generated {len(rows):,} records -> {path}")


# ── Main ────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_OUTPUT_PATH = os.path.join(_SCRIPT_DIR, "data", "cloud_billing_2024.csv")

if __name__ == "__main__":
    data = generate_billing_data()
    save_csv(data, _OUTPUT_PATH)

