SELECT
    i.investor,
    round(sum(i.montante_total)::numeric, 2) AS patrimonio_em_reais
FROM analytics.fct_investments_portfolio i
GROUP BY i.investor
ORDER BY sum(i.montante_total) DESC;


-- To know the latest transaction date
SELECT MAX(transaction_date) FROM postgres_raw.stock_movements;


SELECT * FROM analytics.fct_unified_payments
WHERE payment_type LIKE 'credit_card';

-- To discover the spend made without proper descriptio
SELECT description, COUNT(*), SUM(amount_brl) AS total
FROM analytics.fct_unified_payments
WHERE category_name = 'Não Classificado'
GROUP BY 1
ORDER BY total DESC;

SELECT DISTINCT description
FROM analytics.fct_unified_payments
WHERE category_name = 'Não Classificado'
ORDER BY description ASC;

SELECT 
    payment_id,
    description,
    COUNT(*) as matches_encontrados,
    SUM(amount_brl) as valor_somado_indevido
FROM analytics.fct_unified_payments -- ou fct_unified_payments
GROUP BY 1, 2
HAVING COUNT(*) > 1
ORDER BY matches_encontrados DESC;



