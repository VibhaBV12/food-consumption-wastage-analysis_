SELECT 'date_key' AS checked_key, COUNT(*) AS unmatched_rows
FROM public.stg_canteen s
LEFT JOIN public.dim_date d ON s.date_key = d.date_key
WHERE d.date_key IS NULL

UNION ALL

SELECT 'food_key', COUNT(*)
FROM public.stg_canteen s
LEFT JOIN public.dim_food d ON s.food_key = d.food_key
WHERE d.food_key IS NULL

UNION ALL

SELECT 'meal_key', COUNT(*)
FROM public.stg_canteen s
LEFT JOIN public.dim_meal d ON s.meal_key = d.meal_key
WHERE d.meal_key IS NULL

UNION ALL

SELECT 'canteen_section_key', COUNT(*)
FROM public.stg_canteen s
LEFT JOIN public.dim_canteen_section d
    ON s.canteen_section_key = d.canteen_section_key
WHERE d.canteen_section_key IS NULL;

INSERT INTO public.fact_canteen_waste (
    date_key,
    food_key,
    meal_key,
    canteen_section_key,
    waste_weight_kg,
    unit_price_per_kg,
    cost_loss
)
SELECT
    date_key,
    food_key,
    meal_key,
    canteen_section_key,
    waste_weight_kg,
    unit_price_per_kg,
    cost_loss
FROM public.stg_canteen;
SELECT
    COUNT(*) AS total_records,
    SUM(waste_weight_kg) AS total_waste_kg,
    ROUND(SUM(cost_loss), 2) AS total_cost_loss
FROM public.fact_canteen_waste;
SELECT
    'food_key' AS checked_key,
    COUNT(*) AS unmatched_rows
FROM public.stg_event s
LEFT JOIN public.dim_food d
    ON s.food_key = d.food_key
WHERE d.food_key IS NULL

UNION ALL

SELECT
    'event_context_key',
    COUNT(*)
FROM public.stg_event s
LEFT JOIN public.dim_event_context d
    ON s.event_context_key = d.event_context_key
WHERE d.event_context_key IS NULL;

INSERT INTO public.fact_event_waste (
    event_waste_key,
    food_key,
    event_context_key,
    number_of_guests,
    quantity_of_food,
    wastage_food_amount
)
SELECT
    event_waste_key,
    food_key,
    event_context_key,
    number_of_guests,
    quantity_of_food,
    wastage_food_amount
FROM public.stg_event;
SELECT
    COUNT(*) AS total_records,
    SUM(number_of_guests) AS total_guests,
    SUM(quantity_of_food) AS total_food_quantity,
    SUM(wastage_food_amount) AS total_food_wasted
FROM public.fact_event_waste;

-- Canteen fact table
SELECT
    'Canteen' AS data_source,
    COUNT(*) AS total_records,
    SUM(waste_weight_kg) AS total_food_quantity_kg,
    SUM(cost_loss) AS total_cost_loss
FROM public.fact_canteen_waste

UNION ALL

-- Event fact table
SELECT
    'Event' AS data_source,
    COUNT(*) AS total_records,
    SUM(wastage_food_amount) AS total_food_quantity_kg,
    NULL::NUMERIC AS total_cost_loss
FROM public.fact_event_waste;
SELECT
    COUNT(*) AS total_records,
    SUM(number_of_guests) AS total_guests,
    SUM(quantity_of_food) AS total_food_quantity,
    SUM(wastage_food_amount) AS total_food_wasted
FROM public.fact_event_waste;

SELECT
    'Canteen staging' AS table_name,
    COUNT(*) AS total_records
FROM public.stg_canteen

UNION ALL

SELECT
    'Canteen fact',
    COUNT(*)
FROM public.fact_canteen_waste

UNION ALL

SELECT
    'Event staging',
    COUNT(*)
FROM public.stg_event

UNION ALL

SELECT
    'Event fact',
    COUNT(*)
FROM public.fact_event_waste;

SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

SELECT
    tc.table_name AS fact_table,
    kcu.column_name AS fact_column,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.constraint_schema = kcu.constraint_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON tc.constraint_name = ccu.constraint_name
    AND tc.constraint_schema = ccu.constraint_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name, kcu.column_name;