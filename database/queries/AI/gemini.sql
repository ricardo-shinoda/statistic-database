SELECT * FROM analytics.fct_unified_payments;

SELECT
    purchased_at,
    sum(amount_brl) as total_amount,`   
    description
FROM analytics.fct_unified_payments
WHERE description ilike '%ifd%'
GROUP BY purchased_at, description;

WITH dividendos_mensais AS (
    SELECT
        investor,
        DATE_TRUNC('month', mes_competencia) AS mes_ano,
        SUM(valor_recebido) AS total_mensal
    FROM analytics.fct_investments_dividends
    WHERE investor LIKE 'Casa'
    GROUP BY investor, DATE_TRUNC('month', mes_competencia)
)
SELECT
    EXTRACT(YEAR FROM mes_ano) AS ano,
    ROUND(AVG(total_mensal), 2) AS media_mensal_dividends
FROM dividendos_mensais
GROUP BY EXTRACT(YEAR FROM mes_ano)
ORDER BY ano DESC;

select * from analytics.fct_investments_dividends
where investor like 'Casa';

SELECT * FROM analytics.fct_investments_dividends;


-- Practice Exercises (Exercícios Práticos)
-- Part 1: Unified Payments & Credit Card Statements

-- (Voltado para as tabelas fct_unified_payments e fct_credit_card_statements)

-- English & Adapted: Select the description, amount_brl, and
--  category_name of all payments, ordered by the description in descending order.

-- SELECT * FROM analytics.fct_unified_payments;
SELECT * FROM analytics.fct_unified_payments;

select * from analytics.fct_unified_payments;

select * from analytics.fct_investments;

--         English & Adapted: Find all unique descriptions in credit card 
-- statements that contain the letter "R" (case-insensitive).


--         English & Adapted: Find all rows in unified payments where the
--  category_name starts with the letter "C".


--         English & Adapted: Find all payment entries where the 
-- subcategory_name ends with the letter "A".


--         English & Adapted: Find all transactions where the transaction type 
-- (tipo_gasto) is exactly 'Essencial' (or another category value you frequently use).


--         English & Adapted: Select all payment details where the comments
--  start with the letter "A".


--         English & Adapted: Select only transactions where is_internal_transfer
--  is TRUE.


--         English & Adapted: Find all credit card statement entries where the
--  final_category is NULL.

--         English & Adapted: Select the description and category_name from payments,
--  ordered in ascending order by the category name.

--         English & Adapted: Select all payments where the payment type (payment_type) 
-- is 'Pix' (or 'Credit Card').

-- Part 2: Vehicle Consumption & Investments

-- (Voltado para as tabelas fct_vehicle_consumption e tabelas de investimentos)


--         English & Adapted: Find all vehicle consumption entries where the onboard 
-- computer kilometer reading (onboard_computer_km_l) is not null.


--         English & Adapted: Find all refueling entries where the gas station (gas_station)
--  is 'Ipiranga' (or any other specific station name in your data).


--         English & Adapted: Find all unified payments where the purchase date (purchased_at)
--  is between '2026-01-01' and '2026-06-30' (or any period you want to filter).


--         English & Adapted: Select the ticker and a concatenated string of the investor and
--  their total current equity (e.g., 'Investor: ' || investor || ' | Ticker: ' || ticker) from the investments portfolio table.