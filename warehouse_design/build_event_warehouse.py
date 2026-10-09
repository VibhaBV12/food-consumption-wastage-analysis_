import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

dataset2_path = PROJECT_ROOT / "etl" / "output" / "cleaned_dataset2.csv"
dim_food_path = PROJECT_ROOT / "etl" / "output" / "dim_food.csv"

output_folder = PROJECT_ROOT / "warehouse_design" / "output"

dim_event_context_path = output_folder / "dim_event_context.csv"
fact_event_waste_path = output_folder / "fact_event_waste.csv"


# --------------------------------------------------
# 2. Load the cleaned Dataset 2
# --------------------------------------------------

df = pd.read_csv(dataset2_path)

print("Dataset 2 loaded successfully.")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# --------------------------------------------------
# 3. Load the existing Food Dimension
# --------------------------------------------------

dim_food = pd.read_csv(dim_food_path)

print("\nFood dimension loaded successfully.")
print(dim_food)


# --------------------------------------------------
# 4. Define the Event Context attributes
# --------------------------------------------------

context_columns = [
    "Event_Type",
    "Storage_Conditions",
    "Purchase_History",
    "Seasonality",
    "Preparation_Method",
    "Geographical_Location",
    "Pricing"
]


# --------------------------------------------------
# 5. Create the Event Context Dimension
# --------------------------------------------------

dim_event_context = (
    df[context_columns]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Generate surrogate key
dim_event_context.insert(
    0,
    "event_context_key",
    range(1, len(dim_event_context) + 1)
)


# --------------------------------------------------
# 6. Create Food Key mapping
# --------------------------------------------------

food_mapping = dict(
    zip(
        dim_food["food_name"],
        dim_food["food_key"]
    )
)

df["food_key"] = df["Food_Type"].map(food_mapping)


# --------------------------------------------------
# 7. Create Event Context Key mapping
# --------------------------------------------------

context_mapping = {}

for _, row in dim_event_context.iterrows():

    key = tuple(
        row[column]
        for column in context_columns
    )

    context_mapping[key] = row["event_context_key"]


def get_context_key(row):

    key = tuple(
        row[column]
        for column in context_columns
    )

    return context_mapping[key]


df["event_context_key"] = df.apply(
    get_context_key,
    axis=1
)


# --------------------------------------------------
# 8. Validate the mappings
# --------------------------------------------------

print("\nChecking mappings...")

if df["food_key"].isna().any():
    print("ERROR: Some Food_Type values could not be mapped.")

else:
    print("Food mapping: OK")


if df["event_context_key"].isna().any():
    print("ERROR: Some event contexts could not be mapped.")

else:
    print("Event context mapping: OK")


# --------------------------------------------------
# 9. Create the Fact Table
# --------------------------------------------------

fact_event_waste = df[
    [
        "food_key",
        "event_context_key",
        "Number_of_Guests",
        "Quantity_of_Food",
        "Wastage_Food_Amount"
    ]
].copy()

fact_event_waste.insert(
    0,
    "event_waste_key",
    range(1, len(fact_event_waste) + 1)
)


# --------------------------------------------------
# 10. Save the warehouse tables
# --------------------------------------------------

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

dim_event_context.to_csv(
    dim_event_context_path,
    index=False
)

fact_event_waste.to_csv(
    fact_event_waste_path,
    index=False
)


# --------------------------------------------------
# 11. Final validation
# --------------------------------------------------

print("\n----------------------------------------")
print("WAREHOUSE TABLES CREATED")
print("----------------------------------------")

print("\nDimension: dim_event_context")
print("Rows:", len(dim_event_context))
print("Columns:", list(dim_event_context.columns))

print("\nFact: fact_event_waste")
print("Rows:", len(fact_event_waste))
print("Columns:", list(fact_event_waste.columns))

print("\nOriginal Dataset 2 rows:", len(df))
print("Fact table rows:", len(fact_event_waste))

if len(df) == len(fact_event_waste):
    print("Row count validation: PASSED")
else:
    print("Row count validation: FAILED")

print("\nFiles saved to:")
print(output_folder)

print("\nWAREHOUSE EVENT DESIGN COMPLETE")