# ============================================================
# FOOD CONSUMPTION AND WASTAGE ANALYSIS
# DATA WAREHOUSE DESIGN
# MEMBER 2
# ============================================================


# ============================================================
# 1. DIMENSION TABLES
# ============================================================

dimensions = {

    # --------------------------------------------------------
    # DATE DIMENSION
    # --------------------------------------------------------

    "dim_date": {
        "description": "Date dimension for canteen wastage analysis",

        "grain": "One row represents one calendar date",

        "columns": {

            "date_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Surrogate key identifying the date"
            },

            "Date": {
                "data_type": "DATE",
                "key": "",
                "description": "Actual calendar date"
            },

            "day": {
                "data_type": "INTEGER",
                "key": "",
                "description": "Day of the month"
            },

            "month": {
                "data_type": "INTEGER",
                "key": "",
                "description": "Month number"
            },

            "month_name": {
                "data_type": "VARCHAR(20)",
                "key": "",
                "description": "Name of the month"
            },

            "year": {
                "data_type": "INTEGER",
                "key": "",
                "description": "Calendar year"
            },

            "day_name": {
                "data_type": "VARCHAR(20)",
                "key": "",
                "description": "Name of the day"
            }
        }
    },


    # --------------------------------------------------------
    # FOOD DIMENSION
    # --------------------------------------------------------

    "dim_food": {
        "description": "Food dimension shared by both fact tables",

        "grain": "One row represents one food category/type",

        "columns": {

            "food_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Surrogate key identifying the food"
            },

            "food_name": {
                "data_type": "VARCHAR(50)",
                "key": "",
                "description": "Name of the food category/type"
            }
        }
    },


    # --------------------------------------------------------
    # MEAL DIMENSION
    # --------------------------------------------------------

    "dim_meal": {
        "description": "Meal dimension for canteen wastage",

        "grain": "One row represents one meal type",

        "columns": {

            "meal_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Surrogate key identifying the meal"
            },

            "Meal": {
                "data_type": "VARCHAR(20)",
                "key": "",
                "description": "Meal type such as Breakfast, Lunch or Dinner"
            }
        }
    },


    # --------------------------------------------------------
    # CANTEEN SECTION DIMENSION
    # --------------------------------------------------------

    "dim_canteen_section": {
        "description": "Canteen section dimension",

        "grain": "One row represents one canteen section",

        "columns": {

            "canteen_section_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Surrogate key identifying the canteen section"
            },

            "Canteen_Section": {
                "data_type": "VARCHAR(10)",
                "key": "",
                "description": "Canteen section identifier"
            }
        }
    },


    # --------------------------------------------------------
    # EVENT CONTEXT DIMENSION
    # --------------------------------------------------------

    "dim_event_context": {
        "description": "Event and operational context for event wastage",

        "grain": (
            "One row represents one unique combination of "
            "event and operational conditions"
        ),

        "columns": {

            "event_context_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Surrogate key identifying the event context"
            },

            "Event_Type": {
                "data_type": "VARCHAR(50)",
                "key": "",
                "description": "Type of event"
            },

            "Storage_Conditions": {
                "data_type": "VARCHAR(30)",
                "key": "",
                "description": "Food storage condition"
            },

            "Purchase_History": {
                "data_type": "VARCHAR(30)",
                "key": "",
                "description": "Frequency of food purchasing"
            },

            "Seasonality": {
                "data_type": "VARCHAR(30)",
                "key": "",
                "description": "Season associated with the observation"
            },

            "Preparation_Method": {
                "data_type": "VARCHAR(50)",
                "key": "",
                "description": "Food preparation method"
            },

            "Geographical_Location": {
                "data_type": "VARCHAR(30)",
                "key": "",
                "description": "Geographical classification"
            },

            "Pricing": {
                "data_type": "VARCHAR(20)",
                "key": "",
                "description": "Pricing category"
            }
        }
    }
}


# ============================================================
# 2. FACT TABLES
# ============================================================

facts = {

    # --------------------------------------------------------
    # CANTEEN WASTE FACT
    # --------------------------------------------------------

    "fact_canteen_waste": {

        "description": "Canteen food wastage observations",

        "grain": (
            "One row represents one food-wastage observation "
            "for a date, meal, canteen section and food category"
        ),

        "columns": {

            "date_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_date.date_key",
                "description": "Date associated with the wastage observation"
            },

            "food_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_food.food_key",
                "description": "Food associated with the observation"
            },

            "meal_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_meal.meal_key",
                "description": "Meal associated with the observation"
            },

            "canteen_section_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_canteen_section.canteen_section_key",
                "description": "Canteen section associated with the observation"
            },

            "Waste_Weight_kg": {
                "data_type": "DECIMAL(10,2)",
                "key": "",
                "description": "Amount of food wasted in kilograms"
            },

            "Unit_Price_per_kg": {
                "data_type": "DECIMAL(10,2)",
                "key": "",
                "description": "Price of one kilogram of food"
            },

            "Cost_Loss": {
                "data_type": "DECIMAL(12,2)",
                "key": "",
                "description": "Monetary loss caused by food wastage"
            },

            
            "canteen_waste_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Unique identifier for each canteen waste observation"
            },
        }
    },


    # --------------------------------------------------------
    # EVENT WASTE FACT
    # --------------------------------------------------------

    "fact_event_waste": {

        "description": "Food wastage observations associated with events",

        "grain": (
            "One row represents one food-wastage observation "
            "associated with an event and operational context"
        ),

        "columns": {

            "food_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_food.food_key",
                "description": "Food associated with the observation"
            },

            "event_context_key": {
                "data_type": "INTEGER",
                "key": "FK",
                "references": "dim_event_context.event_context_key",
                "description": "Operational/event context"
            },

            "Number_of_Guests": {
                "data_type": "INTEGER",
                "key": "",
                "description": "Number of guests attending the event"
            },

            "Quantity_of_Food": {
                "data_type": "DECIMAL(10,2)",
                "key": "",
                "description": "Quantity of food prepared or available"
            },

            "Wastage_Food_Amount": {
                "data_type": "DECIMAL(10,2)",
                "key": "",
                "description": "Amount of food wasted"
            },

            
            "event_waste_key": {
                "data_type": "INTEGER",
                "key": "PK",
                "description": "Unique identifier for each event waste observation"
            },
        }
    }
}


# ============================================================
# 3. RELATIONSHIPS
# ============================================================

relationships = [

    {
        "fact_table": "fact_canteen_waste",
        "foreign_key": "date_key",
        "dimension_table": "dim_date",
        "primary_key": "date_key"
    },

    {
        "fact_table": "fact_canteen_waste",
        "foreign_key": "food_key",
        "dimension_table": "dim_food",
        "primary_key": "food_key"
    },

    {
        "fact_table": "fact_canteen_waste",
        "foreign_key": "meal_key",
        "dimension_table": "dim_meal",
        "primary_key": "meal_key"
    },

    {
        "fact_table": "fact_canteen_waste",
        "foreign_key": "canteen_section_key",
        "dimension_table": "dim_canteen_section",
        "primary_key": "canteen_section_key"
    },

    {
        "fact_table": "fact_event_waste",
        "foreign_key": "food_key",
        "dimension_table": "dim_food",
        "primary_key": "food_key"
    },

    {
        "fact_table": "fact_event_waste",
        "foreign_key": "event_context_key",
        "dimension_table": "dim_event_context",
        "primary_key": "event_context_key"
    }
]


# ============================================================
# 4. DISPLAY THE DESIGN
# ============================================================

print("=" * 70)
print("FOOD CONSUMPTION AND WASTAGE ANALYSIS")
print("DATA WAREHOUSE DESIGN")
print("=" * 70)


print("\nDIMENSION TABLES")
print("-" * 70)

for table_name, table_info in dimensions.items():

    print(f"\n{table_name}")
    print(f"Description : {table_info['description']}")
    print(f"Grain       : {table_info['grain']}")

    for column_name, column_info in table_info["columns"].items():

        key = column_info["key"]

        if key:
            print(
                f"  {column_name:<30} "
                f"{column_info['data_type']:<18} "
                f"{key}"
            )
        else:
            print(
                f"  {column_name:<30} "
                f"{column_info['data_type']:<18}"
            )


print("\n\nFACT TABLES")
print("-" * 70)

for table_name, table_info in facts.items():

    print(f"\n{table_name}")
    print(f"Description : {table_info['description']}")
    print(f"Grain       : {table_info['grain']}")

    for column_name, column_info in table_info["columns"].items():

        key = column_info["key"]

        if key:
            print(
                f"  {column_name:<30} "
                f"{column_info['data_type']:<18} "
                f"{key}"
            )
        else:
            print(
                f"  {column_name:<30} "
                f"{column_info['data_type']:<18}"
            )


print("\n\nRELATIONSHIPS")
print("-" * 70)

for relationship in relationships:

    print(
        f"{relationship['fact_table']}."
        f"{relationship['foreign_key']} "
        f"--> "
        f"{relationship['dimension_table']}."
        f"{relationship['primary_key']}"
    )


print("\n")
print("=" * 70)
print("WAREHOUSE DESIGN COMPLETE")
print("=" * 70)