INSERT INTO public.dim_date (
    date_key,
    date,
    day,
    month,
    month_name,
    year,
    day_name
)
SELECT DISTINCT
    date_key,
    date,
    day,
    month,
    month_name,
    year,
    day_name
FROM public.stg_dim_date;

SELECT COUNT(*) AS total_dates
FROM public.dim_date;

SELECT *
FROM public.dim_date
LIMIT 10;


INSERT INTO public.dim_food (
    food_key,
    food_name
)
SELECT DISTINCT
    food_key,
    food_name
FROM public.stg_dim_food;

SELECT COUNT(*) AS total_foods
FROM public.dim_food;

SELECT *
FROM public.dim_food
ORDER BY food_key
LIMIT 10;

INSERT INTO public.dim_meal (
    meal_key,
    meal
)
SELECT DISTINCT
    meal_key,
    meal
FROM public.stg_dim_meal;
SELECT COUNT(*) AS total_meals
FROM public.dim_meal;

SELECT *
FROM public.dim_meal
ORDER BY meal_key;


INSERT INTO public.dim_canteen_section (
    canteen_section_key,
    canteen_section
)
SELECT DISTINCT
    canteen_section_key,
    canteen_section
FROM public.stg_dim_canteen_section;
SELECT COUNT(*) AS total_sections
FROM public.dim_canteen_section;

SELECT *
FROM public.dim_canteen_section
ORDER BY canteen_section_key;

SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN (
      'dim_event_context',
      'stg_dim_event_context'
  )
ORDER BY table_name, ordinal_position;

INSERT INTO public.dim_event_context (
    event_context_key,
    event_type,
    storage_conditions,
    purchase_history,
    seasonality,
    preparation_method,
    geographical_location,
    pricing
)
SELECT DISTINCT
    event_context_key,
    event_type,
    storage_conditions,
    purchase_history,
    seasonality,
    preparation_method,
    geographical_location,
    pricing
FROM public.stg_dim_event_context;
SELECT COUNT(*) AS total_event_contexts
FROM public.dim_event_context;
SELECT *
FROM public.dim_event_context
ORDER BY event_context_key
LIMIT 10;

SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND (
      table_name LIKE '%fact%'
      OR table_name LIKE '%stg_canteen%'
  )
ORDER BY table_name, ordinal_position;

SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name LIKE 'fact%'
ORDER BY table_name, ordinal_position;

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema = 'public'
ORDER BY table_name;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'stg_event'
ORDER BY ordinal_position;