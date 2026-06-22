-- total amount of divideds received by investor
select 
    investor, 
    sum(valor_recebido) as total_proventos_historico
from analytics.fct_investments_dividends
group by investor
order by total_proventos_historico desc;

-- Amount of dividends by month
select 
    mes_competencia,
    investor,
    sum(valor_recebido) as total_mes
from analytics.fct_investments_dividends
group by 1, 2
order by mes_competencia desc, investor;

-- Amount of dividends by month (TBD)
select
    investor,
    month,
    round(sum(total_amount)::numeric, 2) as total_proventos
from postgres_raw.stock_movements
where transaction_type not in ('Compra', 'Venda', 'Calculo IR - Venda', 'Imposto a pagar') -- Garante que só entram rendimentos/entradas
group by investor, month
order by investor ASC, month DESC;

--  Validate total amount of dividends
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

-- Sum dividends by investor
select
    month,
    transaction_date,
    sum(total_amount)
from postgres_raw.stock_movements
where investor like 'Lucas'
AND transaction_type IN ('Dividendo', 'Juros sobre capital', 'Rendimento')
group by month, transaction_date
order by 2 DESC;

SELECT * FROM analytics.fct_investments_dividends;

SELECT
    investor,
    mes_competencia,
    sum(valor_recebido)
from analytics.fct_investments_dividends
group by 2, 1;

SELECT
    initcap(m.investor) as investor,
    month as mes_competencia,
    round(sum(m.total_amount)::numeric, 2) as total_dividendos
FROM postgres_raw.stock_movements m
WHERE trim(lower(m.investor)) in ('lucas', 'luísa', 'ricardo', 'casa')
  AND trim(lower(m.transaction_type)) in (
        'dividendo', 
        'juros sobre capital', 
        'rendimento', 
        'rendimento (dividendo)', 
        'provento frações'
  )
GROUP BY 1, 2
ORDER BY mes_competencia DESC, total_dividendos DESC;


select * from analytics.fct_monthly_investments;