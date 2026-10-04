# Food Wastage Analysis and Decision Support System

## Project Overview

This project develops a Food Waste Analytics and Decision Support System using food wastage, operational, time-based and financial data.

The system aims to identify food wastage patterns, factors associated with higher wastage and financial losses to support better food preparation and purchasing decisions.

## Member 1 — Python / Pandas / ETL

Member 1 is responsible for:

- Loading the datasets
- Inspecting the datasets
- Checking data types
- Checking missing values
- Checking duplicate records
- Standardizing categorical values
- Validating numerical values
- Cleaning and transforming the datasets
- Creating dimension datasets
- Preparing data for PostgreSQL

## Datasets

### Dataset 1 — Canteen Wastage

Contains:

- Date
- Meal
- Canteen Section
- Food Category
- Waste Weight
- Unit Price
- Cost Loss

### Dataset 2 — Event / Operational Wastage

Contains:

- Food Type
- Number of Guests
- Event Type
- Quantity of Food
- Storage Conditions
- Purchase History
- Seasonality
- Preparation Method
- Geographical Location
- Pricing
- Wastage Food Amount

## ETL Process

```text
Raw Datasets
     ↓
Python / Pandas
     ↓
Data Inspection
     ↓
Data Cleaning
     ↓
Data Standardization
     ↓
Data Validation
     ↓
Dimension Creation
     ↓
Cleaned CSV Files
     ↓
PostgreSQL Data Warehouse
     ↓
SQL Analysis
     ↓
Power BI Dashboard
```

## Member 1 Outputs

- cleaned_dataset1.csv
- cleaned_dataset2.csv
- dim_date.csv
- dim_food.csv
- dim_meal.csv
- dim_canteen_section.csv
- fact_canteen_waste.csv
- fact_event_waste.csv
- inspection_summary.csv
- validation_report.csv

## Data Quality Findings

Dataset 1 contains 2,600 rows and no missing or duplicate records.

The supplied Dataset 2 contains 1,782 rows. Inspection identified 164 exact duplicate records. These duplicates were removed during ETL, resulting in 1,618 cleaned records.

## Technologies

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- Power BI
- GitHub
- VS Code