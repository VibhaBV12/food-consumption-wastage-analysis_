SELECT
    meal_key,
    SUM(waste_weight_kg) AS total_waste_kg,
    ROUND(SUM(cost_loss), 2) AS total_cost_loss
FROM public.fact_canteen_waste
GROUP BY meal_key
ORDER BY total_waste_kg DESC;

SELECT
    food_key,
    SUM(waste_weight_kg) AS total_waste_kg,
    ROUND(SUM(cost_loss), 2) AS total_cost_loss
FROM public.fact_canteen_waste
GROUP BY food_key
ORDER BY total_waste_kg DESC;


SELECT
    canteen_section_key,
    SUM(waste_weight_kg) AS total_waste_kg,
    ROUND(SUM(cost_loss), 2) AS total_cost_loss
FROM public.fact_canteen_waste
GROUP BY canteen_section_key
ORDER BY total_waste_kg DESC;

SELECT
    event_context_key,
    COUNT(*) AS event_records,
    SUM(number_of_guests) AS total_guests,
    SUM(quantity_of_food) AS total_food_quantity,
    SUM(wastage_food_amount) AS total_food_wasted
FROM public.fact_event_waste
GROUP BY event_context_key
ORDER BY total_food_wasted DESC;
