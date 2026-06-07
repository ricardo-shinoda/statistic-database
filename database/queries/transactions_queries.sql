-- Total expenses value (monthly)
SELECT 
    CASE 
        WHEN invoice_name LIKE 'Fatura_%' THEN SUBSTRING(invoice_name FROM 8 FOR 7)
        ELSE TO_CHAR(purchased_at, 'YYYY-MM') 
    END AS competencia,
    
    ROUND(SUM(CASE WHEN payment_type = 'credit_card' THEN amount_brl ELSE 0 END)::NUMERIC, 2) AS gasto_cartao,
    
    ROUND(SUM(CASE WHEN payment_type = 'pix' THEN amount_brl ELSE 0 END)::NUMERIC, 2) AS gasto_pix,
    
    ROUND(SUM(amount_brl)::NUMERIC, 2) AS total_consumo_mes,
    
    COUNT(*) AS total_transacoes
FROM analytics.fct_unified_payments
WHERE is_internal_transfer = FALSE 
  AND is_payment_transaction = FALSE
GROUP BY 1
ORDER BY 1 DESC;

SELECT
    *
FROM postgres_raw.stock_movements;

select
    month,
    transaction_date,
    sum(total_amount)
from postgres_raw.stock_movements
where investor like 'Lucas'
AND transaction_type IN ('Dividendo', 'Juros sobre capital', 'Rendimento')
group by month, transaction_date
order by 2 DESC;

select
    investor,
    month,
    transaction_date,
    round(sum(total_amount)::numeric, 2) as total_rendimentos
from postgres_raw.stock_movements
where investor like 'Casa'
  and transaction_type in ('Dividendo', 'Juros sobre capital', 'Rendimento')
group by month, transaction_date, investor
order by 2 desc;