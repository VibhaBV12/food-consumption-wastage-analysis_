CREATE TABLE stg_dim_date (
    date_key INTEGER,
    date DATE,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    year INTEGER,
    day_name VARCHAR(20)
);

CREATE TABLE stg_dim_food (
    food_key INTEGER,
    food_name VARCHAR(50)
);

CREATE TABLE stg_dim_meal (
    meal_key INTEGER,
    meal VARCHAR(20)
);

CREATE TABLE stg_dim_canteen_section (
    canteen_section_key INTEGER,
    canteen_section VARCHAR(10)
);

CREATE TABLE stg_dim_event_context (
    event_context_key INTEGER,
    event_type VARCHAR(50),
    storage_conditions VARCHAR(30),
    purchase_history VARCHAR(30),
    seasonality VARCHAR(30),
    preparation_method VARCHAR(50),
    geographical_location VARCHAR(30),
    pricing VARCHAR(20)
);

CREATE TABLE stg_canteen (
    date_key INTEGER,
    food_key INTEGER,
    meal_key INTEGER,
    canteen_section_key INTEGER,
    date DATE,
    meal VARCHAR(20),
    canteen_section VARCHAR(10),
    food_category VARCHAR(50),
    waste_weight_kg NUMERIC(10,2),
    unit_price_per_kg NUMERIC(10,2),
    cost_loss NUMERIC(12,2)
);

CREATE TABLE stg_event (
    event_waste_key INTEGER,
    food_key INTEGER,
    event_context_key INTEGER,
    number_of_guests INTEGER,
    quantity_of_food NUMERIC(10,2),
    wastage_food_amount NUMERIC(10,2)
);
SELECT COUNT(*) FROM stg_dim_canteen_section;

SELECT *
FROM public.stg_dim_canteen_section;
SELECT * 
FROM stg_dim_meal
LIMIT 10;

SELECT 'stg_dim_date' AS table_name, COUNT(*) AS row_count
FROM public.stg_dim_date

UNION ALL

SELECT 'stg_dim_food', COUNT(*)
FROM public.stg_dim_food

UNION ALL

SELECT 'stg_dim_meal', COUNT(*)
FROM public.stg_dim_meal

UNION ALL

SELECT 'stg_dim_canteen_section', COUNT(*)
FROM public.stg_dim_canteen_section

UNION ALL

SELECT 'stg_dim_event_context', COUNT(*)
FROM public.stg_dim_event_context

UNION ALL

SELECT 'stg_canteen', COUNT(*)
FROM public.stg_canteen

UNION ALL

SELECT 'stg_event', COUNT(*)
FROM public.stg_event;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- 1. Date dimension
CREATE TABLE IF NOT EXISTS public.dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    year INTEGER,
    day_name VARCHAR(20)
);

-- 2. Food dimension
CREATE TABLE IF NOT EXISTS public.dim_food (
    food_key INTEGER PRIMARY KEY,
    food_name VARCHAR(50)
);

-- 3. Meal dimension
CREATE TABLE IF NOT EXISTS public.dim_meal (
    meal_key INTEGER PRIMARY KEY,
    meal VARCHAR(20)
);

-- 4. Canteen section dimension
CREATE TABLE IF NOT EXISTS public.dim_canteen_section (
    canteen_section_key INTEGER PRIMARY KEY,
    canteen_section VARCHAR(10)
);

-- 5. Event context dimension
CREATE TABLE IF NOT EXISTS public.dim_event_context (
    event_context_key INTEGER PRIMARY KEY,
    event_type VARCHAR(50),
    storage_conditions VARCHAR(30),
    purchase_history VARCHAR(30),
    seasonality VARCHAR(30),
    preparation_method VARCHAR(50),
    geographical_location VARCHAR(30),
    pricing VARCHAR(20)
);

