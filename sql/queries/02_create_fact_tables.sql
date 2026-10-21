CREATE TABLE public.fact_canteen_waste (
    canteen_waste_key SERIAL PRIMARY KEY,
    date_key INTEGER REFERENCES public.dim_date(date_key),
    food_key INTEGER REFERENCES public.dim_food(food_key),
    meal_key INTEGER REFERENCES public.dim_meal(meal_key),
    canteen_section_key INTEGER
        REFERENCES public.dim_canteen_section(canteen_section_key),
    waste_weight_kg NUMERIC,
    unit_price_per_kg NUMERIC,
    cost_loss NUMERIC
);
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name = 'fact_canteen_waste';

CREATE TABLE public.fact_event_waste (
    event_waste_key INTEGER PRIMARY KEY,
    food_key INTEGER REFERENCES public.dim_food(food_key),
    event_context_key INTEGER
        REFERENCES public.dim_event_context(event_context_key),
    number_of_guests INTEGER,
    quantity_of_food NUMERIC,
    wastage_food_amount NUMERIC
);
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('fact_canteen_waste', 'fact_event_waste')
ORDER BY table_name;

