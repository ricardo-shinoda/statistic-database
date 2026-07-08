SELECT
    *
FROM postgres_raw.stock_movements;



select * from analytics.fct_lucas_investments;

SELECT * FROM analytics.fct_investments_dividends;
select * from analytics.fct_investments_portfolio;

SELECT
    i.investor,
    -- 🔢 Apenas o número puro com duas casas decimais
    round(sum(i.montante_total)::numeric, 2) as patrimonio_em_reais
FROM analytics.fct_investments_portfolio i
GROUP BY i.investor
ORDER BY sum(i.montante_total) DESC;


-- To know the latest transaction date
SELECT MAX(transaction_date) FROM postgres_raw.stock_movements;


select * from analytics.fct_unified_payments
where payment_type like 'credit_card';

-- To discover the spend made without proper descriptio
SELECT description, COUNT(*), SUM(amount_brl) as total
FROM analytics.fct_unified_payments
WHERE category_name = 'Não Classificado'
GROUP BY 1
ORDER BY total DESC;

SELECT DISTINCT description
FROM analytics.fct_unified_payments
WHERE category_name = 'Não Classificado'
ORDER BY description ASC;



