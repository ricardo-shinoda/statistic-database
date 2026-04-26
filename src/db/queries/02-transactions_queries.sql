select * from dim_merchant_mapping;

-- Check total count and date range to ensure 2019 data is there
SELECT 
    MIN(transaction_date) as earliest, 
    MAX(transaction_date) as latest, 
    COUNT(*) as total_rows,
    transaction_type
FROM fact_transactions
GROUP BY transaction_type;

-- Look for any rows where we had to "impute" the description
SELECT * FROM fact_transactions 
WHERE description = 'MISSING_DESCRIPTION';


select * From fact_transactions
where source_file = 'invoice-2019-12.csv'
order by transaction_date ASC;

-- To see which manual bills were added today:
SELECT description, amount_brl, updated_at 
FROM fact_transactions 
WHERE transaction_type = 'manual_bill'
ORDER BY updated_at DESC;

SELECT * FROM fact_transactions 
WHERE description ILIKE '%Coffee%' 
   OR description ILIKE '%Café%';

SELECT 
    ticker, 
    asset_type, 
    SUM(total_amount) as total_investido,
    COUNT(*) as qtd_movimentacoes
FROM fact_investments
GROUP BY ticker, asset_type
ORDER BY asset_type DESC, total_investido DESC;

SELECT 
    owner,
    ticker, 
    asset_type, 
    transaction_type,
    total_amount,
    transaction_date
FROM fact_investments 
ORDER BY transaction_date DESC 
LIMIT 20;

select * From fact_investments
where ticker = 'BITCOIN';

select * from fact_investments
where transaction_type = 'venda';

select * from fact_market_items;

SELECT 
    p.category, 
    SUM(f.total_price_final) as gasto_total
FROM fact_market_items f
JOIN dim_product p ON f.product_code = p.product_code
GROUP BY p.category
ORDER BY gasto_total DESC;

select * from dim_market;
SELECT * FROM fact_investments;
select * from fact_transactions
where transaction_type <> 'manual_bill'
ORDER BY category;
select * From fact_vehicle_fueling;

select count(transaction_date) From fact_transactions;
SELECT * FROM fact_transactions;
select distinct description from fact_transactions
where category = 'Empresa para empresa';

select * from fact_transactions
where installment <> NULL;

select * from stg_credit_card;
select * from pagamento_cartao;
select * from pagamento_dinheiro;

SELECT
    DISTINCT descricao,
    categoria
FROM pagamento_cartao;

select * from postgres_raw.nissan_kicks_consumption;


WITH combined_expenses AS (
    -- Data from the credit card table
    SELECT 
        DATE_TRUNC('month', data_compra) AS mes,
        COALESCE(valor_brl, 0) AS valor_total
    FROM pagamento_cartao
    
    UNION ALL
    
    -- Data from the second table (pagamento_dinheiro)
    SELECT 
        DATE_TRUNC('month', data_compra) AS mes,
        COALESCE(valor, 0) AS valor_total
    FROM pagamento_dinheiro
    WHERE descricao NOT LIKE '%C6%'
        AND descricao NOT LIKE '%C6%'
)
SELECT 
    TO_CHAR(mes, 'YYYY-MM') AS periodo,
    SUM(valor_total) AS total_gasto
FROM combined_expenses
GROUP BY mes
ORDER BY mes DESC;

SELECT 
        DATE_TRUNC('month', data_compra) AS mes,
        SUM(valor_brl) AS valor_total
    FROM pagamento_cartao
GROUP BY mes, sum(valor_brl)
ORDER BY mes DESC;

SELECT 
    TO_CHAR(DATE_TRUNC('month', data_compra), 'YYYY-MM') AS periodo,
    SUM(valor_brl) AS total_cartao,
    COUNT(*) AS num_transacoes
FROM pagamento_cartao
WHERE data_compra >= '2026-01-01'
GROUP BY 1
ORDER BY 1 DESC;


WITH combined_expenses AS (
    -- 1. Credit Card: Individual purchases
    SELECT 
        DATE_TRUNC('month', data_compra) AS mes,
        COALESCE(valor_brl, 0) AS valor_total
    FROM pagamento_cartao
    
    UNION ALL
    
    -- 2. Cash/Debit: Purchases ONLY (Excluding Invoice Payments and C6)
    SELECT 
        DATE_TRUNC('month', data_compra) AS mes,
        COALESCE(valor, 0) AS valor_total
    FROM pagamento_dinheiro
    WHERE 
        -- Exclude C6
        (metodo_pagamento NOT ILIKE '%C6%' OR metodo_pagamento IS NULL)
        -- Exclude Invoice Payments (Adjust these keywords to match your bank's description)
        AND descricao NOT ILIKE '%pagamento%efetuado%'
        AND descricao NOT ILIKE '%fatura%cartao%'
        AND descricao NOT ILIKE '%nubank%' -- common if paying from another account
)
SELECT 
    TO_CHAR(mes, 'YYYY-MM') AS periodo,
    SUM(valor_total) AS total_gasto
FROM combined_expenses
GROUP BY mes
ORDER BY mes DESC;

select * from pagamento_cartao;

-- to get the monthly expend by card
WITH devided_car AS (
    SELECT
        -- DATE_TRUNC('month', data_compra) as mes,
        data_compra,
        COALESCE(valor_brl, 0) as valor,
        cartao_titular,
        cartao_final,
        parcela
    from pagamento_cartao
    where 
        cartao_final ILIKE '7757'
        -- AND data_compra = '2026-03-01' AND data_compra = '2026-03-30'
)




select
    -- TO_CHAR(mes, 'YYYY-MM') as mes,
    data_compra,
    sum(valor) as valor_total,
    cartao_final,
    parcela
from devided_car
group by data_compra, cartao_final, parcela
order by data_compra;


select * from analytics.fact_pagamentos_unificados limit 10;

select * from analytics.fact_unified_payments;

select * from analytics.category_mapping limit 10;

SELECT * FROM analytics.payments LIMIT 100;

select * from postgres_raw.pagamento_dinheiro;

SELECT 
    category_name, 
    COUNT(*) as total_transacoes, 
    SUM(amount_brl) as valor_total
FROM analytics.fact_unified_payments
GROUP BY 1
ORDER BY valor_total DESC;


select * from postgres_raw.stock_movements;

select * From postgres_raw.nissan_kicks_consumption;

SELECT 
    filled_at,
    odometer,
    km_driven,
    liters,
    km_per_liter,
    cost_per_km
FROM analytics.fact_vehicle_consumption
ORDER BY filled_at DESC;

SELECT schema_name, table_name 
FROM information_schema.tables 
WHERE table_name = 'fact_investments';



drop table analytics.fact_investiments;

-- Deleting the Schema postgres_raw to run the new python code from scratch and avoid any duplicated data.
drop schema if exists postgres_raw cascade;
-- Recreating the Schema again
create schema postgres_raw;