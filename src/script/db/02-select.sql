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