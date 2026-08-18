-- Practice Exercises (Exercícios Práticos)
-- Part 1: Unified Payments & Credit Card Statements

-- (Voltado para as tabelas fct_unified_payments e fct_credit_card_statements)

-- Select the description, amount_brl, and
--  category_name of all payments, ordered by the description in descending order.
SELECT * FROM analytics.fct_unified_payments;

SELECT
    description,
    amount_brl,
    category_name
FROM analytics.fct_unified_payments
ORDER BY description DESC;

-- Find all unique descriptions in credit card 
-- statements that contain the letter "R" (case-insensitive).
SELECT * FROM analytics.fct_credit_card_statements;
SELECT 
    DISTINCT description
FROM analytics.fct_credit_card_statements
WHERE description ILIKE '%r%';

-- Find all rows in unified payments where the
--  category_name starts with the letter "C".
SELECT * FROM analytics.fct_unified_payments
WHERE category_name ILIKE 'c%';

-- Find all payment entries where the 
-- subcategory_name ends with the letter "A".
SELECT * FROM analytics.fct_unified_payments
WHERE subcategory_name ILIKE '%a';

-- Find all transactions where the transaction type 
-- (tipo_gasto) is exactly 'Essencial' (or another category value you frequently use).
SELECT * FROM analytics.fct_unified_payments
WHERE tipo_gasto LIKE 'Essencial';

-- Select all payment details where the comments
--  start with the letter "A".
SELECT * FROM analytics.fct_unified_payments
WHERE comments ILIKE 'a%';

-- Select only transactions where is_internal_transfer is TRUE.
SELECT * FROM analytics.fct_unified_payments
WHERE is_internal_transfer LIKE TRUE;

-- Find all credit card statement entries where the
--  final_category is NULL.
SELECT * FROM analytics.fct_credit_card_statements
WHERE final_category IS NULL;

SELECT * FROM analytics.fct_credit_card_statements;

-- Select the description and category_name from payments,
--  ordered in ascending order by the category name.
SELECT
    description,
    category_name
FROM analytics.fct_unified_payments
ORDER BY category_name ASC;

-- Select all payments where the payment type (payment_type) 
-- is 'Pix' (or 'Credit Card').
SELECT * FROM analytics.fct_unified_payments
WHERE payment_type = 'credit_card' OR payment_type = 'pix';

-- Part 2: Vehicle Consumption & Investments
-- (Voltado para as tabelas fct_vehicle_consumption e tabelas de investimentos)

-- Find all vehicle consumption entries where the onboard 
-- computer kilometer reading (onboard_computer_km_l) is not null.
SELECT * FROM analytics.fct_vehicle_consumption
WHERE onboard_computer_km_l IS NOT NULL;

-- Find all refueling entries where the gas station (gas_station)
--  is 'Ipiranga' (or any other specific station name in your data).
SELECT * FROM analytics.fct_vehicle_consumption
WHERE gas_station ILIKE '%ipiranga%';

-- Find all unified payments where the purchase date (purchased_at)
--  is between '2026-01-01' and '2026-06-30' (or any period you want to filter).
SELECT * FROM analytics.fct_unified_payments
WHERE purchased_at between '2026-01-01' AND '2026-06-30';

-- Select the ticker and a concatenated string of the investor and
--  their total current equity (e.g., 'Investor: ' || investor || '  Ticker: ' || ticker) from the investments portfolio table.
SELECT
    CONCAT ('investor: ' || investor || '|' || 'Ticker: ' || ticker)
FROM analytics.fct_investments_dividends;

-- PRACTICE EXERCISES
-- Simple Queries

-- Select only the name of all unique investors in alphabetical order.
SELECT
    DISTINCT investor
FROM analytics.fct_investments_dividends
ORDER BY investor ASC;

-- Select the investment tickers where the average buy price is greater than R$200.00, in ascending order by price.
WITH tirando_media AS (
    SELECT
        ticker,
        round(avg(preco_atual), 2) as media_preco
    FROM analytics.fct_investments_portfolio
    GROUP BY ticker
)

SELECT *
FROM tirando_media
WHERE media_preco > 200;

select * from analytics.fct_investments_portfolio;

-- Select the investment ticker, the current price, and the price adjusted with a 10% increase, 
-- ordered alphabetically by ticker.
SELECT
    ticker,
    preco_atual,
    (preco_atual * 1.10) as adjusted_price
FROM analytics.fct_investments_portfolio;

-- Select all unique gas stations in your vehicle consumption table that are 
-- located in the state of 'Rio Grande do Sul' (or any specific region name).
SELECT
    DISTINCT gas_station
FROM analytics.fct_vehicle_consumption;


-- Select all payment transactions made between '2026-04-10' and '2026-04-25', ordered by amount.

-- Select all payment transactions where the amount is between R1,000.00andR1,500.00.

-- Select all payment transactions where the amount is not between R100.00andR500.00.

-- Select all transactions of payment type 'Credit Card' ordered by amount in descending order.

-- Select all dividend payments received by investor 'Lucas' (or any specific investor) ordered by the received amount in ascending order.

-- Select all transactions from the 'Essential' expense type (tipo_gasto) that were categorized under 'Supermarket' (or any specific category).

-- Select all payment transactions that were processed using the payment type 'Pix'.

-- Select all transactions categorized as either 'Leisure' or 'Home' under your category name.

-- Select all vehicle refuelings made at gas stations named 'Ipiranga' or 'Petrobras'.

-- Select all vehicle refuelings that were not made at gas stations named 'Ipiranga' nor 'Petrobras'.

-- Select all unified payment transactions where the comments column is empty (NULL).

-- Select all credit card statements where the transaction description contains the word 'App' or 'Delivery'.

-- Select all unique investment companies whose names start with the letter 'S'.

-- Select all investment tickers that end with the letter 'A' (e.g., 'PETR4', 'VALE3').

-- Select all investment companies whose names do not start with the letter 'A'.

-- Select all unique gas stations that start with the letter 'P' and are located in the region of 'Santa Catarina'.

-- Select all dividend payouts where the competence month (mes_competencia) is provided (is not NULL).

-- Select all line-item details belonging to payment ID '01'.

-- Select all line-item details belonging to payment ID '06' or payment ID '10'.