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
select * from fact_transactions where transaction_type <> 'manual_bill';
select * From fact_vehicle_fueling;