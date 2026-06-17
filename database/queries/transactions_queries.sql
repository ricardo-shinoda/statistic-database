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


select
    investor,
    month,
    round(sum(total_amount)::numeric, 2) as total_proventos
from postgres_raw.stock_movements
where transaction_type not in ('Compra', 'Venda', 'Calculo IR - Venda', 'Imposto a pagar') -- Garante que só entram rendimentos/entradas
group by investor, month
order by investor ASC, month DESC;

select
    investor,
    round(
        sum(
            case 
                when transaction_type = 'Compra' then total_amount
                when transaction_type = 'Venda' then -total_amount
                else 0 
            end
        )::numeric, 2
    ) as saldo_liquido_aportado
from postgres_raw.stock_movements
group by investor
order by saldo_liquido_aportado DESC;



with total_investimentos_c6 as (
    select
        investor,
        coalesce(sum(
            case 
                when transaction_type = 'Compra' then total_amount
                when transaction_type = 'Venda' then -total_amount
                else 0 
            end
        ), 0) as total_cdb_c6
    from postgres_raw.stock_movements
    where ticker = 'CDB' 
      and organization = 'Banco C6'
    group by investor
),

total_saidas as (
    select
        investor,
        coalesce(sum(total_amount), 0) as total_pago
    from postgres_raw.stg_card_payments -- Ajustado para a sua tabela de staging de pagamentos raw
    group by investor
),

total_entradas as (
    select
        investor,
        coalesce(sum(total_amount), 0) as total_recebido
    from postgres_raw.stg_income -- Ajustado para a sua tabela de staging de entradas raw
    group by investor
)

select
    entradas.investor,
    round(entradas.total_recebido::numeric, 2) as mais_total_entradas,
    round(coalesce(inv.total_cdb_c6, 0)::numeric, 2) as mais_total_cdb_c6,
    round(coalesce(saidas.total_pago, 0)::numeric, 2) as menos_total_saidas,
    round(
        (entradas.total_recebido + coalesce(inv.total_cdb_c6, 0) - coalesce(saidas.total_pago, 0))::numeric, 2
    ) as saldo_atual_calculado
from total_entradas entradas
left join total_investimentos_c6 inv on entradas.investor = inv.investor
left join total_saidas saidas on entradas.investor = saidas.investor
order by saldo_atual_calculado DESC;


select
    investor,
    ticker,
    sum(
        case 
            when transaction_type = 'Compra' then quantity
            when transaction_type = 'Venda' then -quantity
            else 0 
        end
    ) as quantidade_cotas_atual
from postgres_raw.stock_movements
where investor = 'Lucas'
group by investor, ticker;

select * from analytics.fct_lucas_investments;

select * from analytics.fct_investments_portfolio;

SELECT * FROM analytics.fct_investments_dividends;


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
