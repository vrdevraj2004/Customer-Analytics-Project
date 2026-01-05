-- Create view with age_group
CREATE OR REPLACE VIEW customer_with_age_group AS
SELECT *,
       CASE 
           WHEN age BETWEEN 18 AND 25 THEN '18-25'
           WHEN age BETWEEN 26 AND 35 THEN '26-35'
           WHEN age BETWEEN 36 AND 45 THEN '36-45'
           WHEN age BETWEEN 46 AND 60 THEN '46-60'
           ELSE '60+' 
       END AS age_group
FROM customer;


-- Most popular product by gender
SELECT gender, item_purchased, COUNT(*) AS total_purchases
FROM customer_with_age_group
GROUP BY gender, item_purchased
ORDER BY gender, total_purchases DESC;


-- Highest revenue-generating product for males vs females
SELECT gender, item_purchased, SUM(purchase_amount) AS total_revenue
FROM customer_with_age_group
GROUP BY gender, item_purchased
ORDER BY gender, total_revenue DESC;


-- Average review rating by age group
SELECT age_group, ROUND(AVG(review_rating)::numeric,2) AS avg_rating
FROM customer_with_age_group
GROUP BY age_group
ORDER BY avg_rating DESC;


-- Category with highest percentage of purchases with discounts applied
SELECT category,
       ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS discount_rate
FROM customer_with_age_group
GROUP BY category
ORDER BY discount_rate DESC;


-- Most loyal age group (based on previous purchases)
SELECT age_group, SUM(previous_purchases) AS total_previous_purchases
FROM customer_with_age_group
GROUP BY age_group
ORDER BY total_previous_purchases DESC;


-- Average spending per product category for males vs females
SELECT gender, category, ROUND(AVG(purchase_amount),2) AS avg_spend
FROM customer_with_age_group
GROUP BY gender, category
ORDER BY gender, avg_spend DESC;


-- Top 3 products per age group
WITH product_counts AS (
    SELECT age_group, item_purchased,
           COUNT(*) AS total_orders,
           ROW_NUMBER() OVER (PARTITION BY age_group ORDER BY COUNT(*) DESC) AS rank
    FROM customer_with_age_group
    GROUP BY age_group, item_purchased
)
SELECT age_group, item_purchased, total_orders
FROM product_counts
WHERE rank <= 3
ORDER BY age_group, total_orders DESC;


-- Which gender uses discounts more frequently
SELECT gender,
       ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS discount_rate
FROM customer_with_age_group
GROUP BY gender
ORDER BY discount_rate DESC;

-- Top product per month by revenue
WITH monthly_product_revenue AS (
    SELECT month,
           item_purchased,
           SUM(purchase_amount) AS total_revenue,
           ROW_NUMBER() OVER (PARTITION BY month ORDER BY SUM(purchase_amount) DESC) AS rank
    FROM customer_with_age_group
    GROUP BY month, item_purchased
)
SELECT month, item_purchased, total_revenue
FROM monthly_product_revenue
WHERE rank = 1
ORDER BY month;

-- Total revenue per category
SELECT category,
       SUM(purchase_amount) AS total_revenue,
       ROUND(AVG(purchase_amount),2) AS avg_purchase
FROM customer_with_age_group
GROUP BY category
ORDER BY total_revenue DESC;



-- Quick preview of the first 10 rows
SELECT * FROM customer_with_age_group LIMIT 50;
