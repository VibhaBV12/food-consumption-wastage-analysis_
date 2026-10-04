"""
Member 1 - Food Waste Analytics & Decision Support System
Python / Pandas / ETL

Inputs:
  Dataset_1.csv.xlsx  -> Canteen wastage dataset
  Dataset_2.xlxs.csv  -> Event/operational food wastage dataset

Run:
  python etl_dataset1.py

Outputs are written to the output/ directory.
"""

from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)

DATASET_1 = BASE.parent / "data" / "Dataset_1.csv.xlsx"
DATASET_2 = BASE.parent / "data" / "Dataset_2.xlxs.csv"



def inspect_dataset(df, name):
    report = {
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_cells": int(df.isna().sum().sum()),
    }

    for col in df.columns:
        report[f"missing__{col}"] = int(df[col].isna().sum())
        report[f"unique__{col}"] = int(df[col].nunique(dropna=True))

    return report


def clean_text_columns(df):
    df = df.copy()
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()
    return df


def clean_dataset_1(df):
    df = clean_text_columns(df)

    # Standardize date and categorical columns.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in ["Meal", "Canteen_Section", "Food_Category"]:
        df[col] = df[col].str.title()

    # Numeric conversion and validation.
    numeric_cols = ["Waste_Weight_kg", "Unit_Price_per_kg", "Cost_Loss"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows with invalid required values.
    df = df.dropna(subset=["Date", "Meal", "Canteen_Section",
                           "Food_Category"] + numeric_cols)

    # Keep only physically meaningful values.
    df = df[
        (df["Waste_Weight_kg"] >= 0)
        & (df["Unit_Price_per_kg"] >= 0)
        & (df["Cost_Loss"] >= 0)
    ]

    # Source contains monetary values rounded to 2 decimals.
    # Recalculate and round only where the difference exceeds 0.01.
    expected_loss = (df["Waste_Weight_kg"] * df["Unit_Price_per_kg"]).round(2)
    mismatch = (expected_loss - df["Cost_Loss"]).abs() > 0.01
    df.loc[mismatch, "Cost_Loss"] = expected_loss[mismatch]

    # Date attributes for the warehouse dimension.
    df["Date"] = df["Date"].dt.normalize()

    return df.drop_duplicates().sort_values("Date").reset_index(drop=True)


def clean_dataset_2(df):
    df = clean_text_columns(df)

    rename_map = {
        "Type of Food": "Food_Type",
        "Number of Guests": "Number_of_Guests",
        "Event Type": "Event_Type",
        "Quantity of Food": "Quantity_of_Food",
        "Storage Conditions": "Storage_Conditions",
        "Purchase History": "Purchase_History",
        "Seasonality": "Seasonality",
        "Preparation Method": "Preparation_Method",
        "Geographical Location": "Geographical_Location",
        "Pricing": "Pricing",
        "Wastage Food Amount": "Wastage_Food_Amount",
    }
    df = df.rename(columns=rename_map)

    categorical = [
        "Food_Type", "Event_Type", "Storage_Conditions", "Purchase_History",
        "Seasonality", "Preparation_Method", "Geographical_Location", "Pricing"
    ]
    for col in categorical:
        df[col] = df[col].str.title()

    numeric = ["Number_of_Guests", "Quantity_of_Food", "Wastage_Food_Amount"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=categorical + numeric)
    df = df[
        (df["Number_of_Guests"] >= 0)
        & (df["Quantity_of_Food"] >= 0)
        & (df["Wastage_Food_Amount"] >= 0)
        & (df["Wastage_Food_Amount"] <= df["Quantity_of_Food"])
    ]

    # Duplicate event records are removed because they are exact duplicate rows
    # and there is no event/date identifier in the source to distinguish them.
    return df.drop_duplicates().reset_index(drop=True)


def make_dimensions(d1, d2):
    dim_date = (
        d1[["Date"]].drop_duplicates()
        .sort_values("Date")
        .reset_index(drop=True)
    )
    dim_date.insert(0, "date_key", range(1, len(dim_date) + 1))
    dim_date["day"] = dim_date["Date"].dt.day
    dim_date["month"] = dim_date["Date"].dt.month
    dim_date["month_name"] = dim_date["Date"].dt.strftime("%B")
    dim_date["year"] = dim_date["Date"].dt.year
    dim_date["day_name"] = dim_date["Date"].dt.strftime("%A")

    # Combine food names/categories from both datasets into one reusable dimension.
    food_names = sorted(set(d1["Food_Category"].dropna()) | set(d2["Food_Type"].dropna()))
    dim_food = pd.DataFrame({
        "food_key": range(1, len(food_names) + 1),
        "food_name": food_names
    })

    dim_meal = pd.DataFrame({
        "meal_key": range(1, d1["Meal"].nunique() + 1),
        "Meal": sorted(d1["Meal"].unique())
    })

    dim_section = pd.DataFrame({
        "canteen_section_key": range(1, d1["Canteen_Section"].nunique() + 1),
        "Canteen_Section": sorted(d1["Canteen_Section"].unique())
    })

    return dim_date, dim_food, dim_meal, dim_section


def add_dimension_keys(d1, dim_date, dim_food, dim_meal, dim_section):
    fact = d1.merge(dim_date[["date_key", "Date"]], on="Date", how="left")

    food_lookup = dim_food.rename(columns={"food_name": "Food_Category"})
    fact = fact.merge(food_lookup, on="Food_Category", how="left")
    fact = fact.merge(dim_meal, on="Meal", how="left")
    fact = fact.merge(dim_section, on="Canteen_Section", how="left")

    fact = fact[
        [
            "date_key", "food_key", "meal_key", "canteen_section_key",
            "Date", "Meal", "Canteen_Section", "Food_Category",
            "Waste_Weight_kg", "Unit_Price_per_kg", "Cost_Loss"
        ]
    ]
    return fact


def main():
    d1_raw = pd.read_excel(DATASET_1)
    d2_raw = pd.read_csv(DATASET_2)

    inspection = pd.DataFrame([
        inspect_dataset(d1_raw, "Dataset 1 - Canteen Wastage"),
        inspect_dataset(d2_raw, "Dataset 2 - Event/Operational Wastage"),
    ])
    inspection.to_csv(OUTPUT / "inspection_summary.csv", index=False)

    d1 = clean_dataset_1(d1_raw)
    d2 = clean_dataset_2(d2_raw)

    d1.to_csv(OUTPUT / "cleaned_dataset1.csv", index=False)
    d2.to_csv(OUTPUT / "cleaned_dataset2.csv", index=False)

    dim_date, dim_food, dim_meal, dim_section = make_dimensions(d1, d2)
    dim_date.to_csv(OUTPUT / "dim_date.csv", index=False)
    dim_food.to_csv(OUTPUT / "dim_food.csv", index=False)
    dim_meal.to_csv(OUTPUT / "dim_meal.csv", index=False)
    dim_section.to_csv(OUTPUT / "dim_canteen_section.csv", index=False)

    fact_canteen = add_dimension_keys(
        d1, dim_date, dim_food, dim_meal, dim_section
    )
    fact_canteen.to_csv(OUTPUT / "fact_canteen_waste.csv", index=False)

    # Dataset 2 is kept at its original grain because it has no date field.
    d2.to_csv(OUTPUT / "fact_event_waste.csv", index=False)

    validation = pd.DataFrame({
        "check": [
            "Dataset 1 cleaned rows",
            "Dataset 2 raw rows",
            "Dataset 2 cleaned rows",
            "Dataset 1 cleaned missing cells",
            "Dataset 2 cleaned missing cells",
            "Dataset 1 duplicate rows after cleaning",
            "Dataset 2 duplicate rows after cleaning",
        ],
        "value": [
            len(d1),
            len(d2_raw),
            len(d2),
            int(d1.isna().sum().sum()),
            int(d2.isna().sum().sum()),
            int(d1.duplicated().sum()),
            int(d2.duplicated().sum()),
        ]
    })
    validation.to_csv(OUTPUT / "validation_report.csv", index=False)

    print("ETL completed successfully.")
    print(f"Dataset 1: {len(d1_raw)} raw -> {len(d1)} cleaned rows")
    print(f"Dataset 2: {len(d2_raw)} raw -> {len(d2)} cleaned rows")
    print(f"Outputs: {OUTPUT}")


if __name__ == "__main__":
    main()
