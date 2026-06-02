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

select * From postgres_raw.purchases;


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

DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
DROP SCHEMA IF EXISTS analytics CASCADE;
CREATE SCHEMA analytics;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'postgres_raw';

select * from postgres_raw.payment_card;

DROP schema analytics cascade;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'postgres_raw';

select * from analytics.fact_credit_card_statements;

-- Montante gasto por mês (ano + mês)
SELECT 
    DATE_TRUNC('month', purchased_at) AS mes,
    TO_CHAR(DATE_TRUNC('month', purchased_at), 'YYYY-MM') AS ano_mes,
    SUM(amount_brl) AS total_gasto_mes,
    COUNT(*) AS quantidade_transacoes
    -- SUM(amount_brl) / COUNT(*) AS ticket_medio
FROM analytics.fact_credit_card_statements
WHERE DATE_TRUNC('month', purchased_at) = DATE_TRUNC('month', '2026-04-01'::DATE);
-- GROUP BY DATE_TRUNC('month', purchased_at)
-- ORDER BY DATE_TRUNC('month', purchased_at) DESC;

select 
    DATE_TRUNC('month', purchased_at) AS mes
    sum(am)
from analytics.fact_credit_card_statements;

-- Ver todas as transações do mês com problema, ordenadas por valor
SELECT 
    purchased_at,
    description,
    amount_brl,
    final_category,
    CASE 
        WHEN amount_brl < 0 THEN 'CREDITO/ESTORNO'
        ELSE 'DEBITO'
    END AS tipo_lancamento
FROM analytics.fact_credit_card_statements
WHERE DATE_TRUNC('month', purchased_at) = DATE_TRUNC('month', '2026-04-01'::DATE)  -- ajuste o mês
ORDER BY amount_brl ASC;  -- valores negativos primeiro

SELECT 
    DATE_TRUNC('month', purchased_at) AS mes,
    TO_CHAR(DATE_TRUNC('month', purchased_at), 'YYYY-MM') AS ano_mes,
    SUM(CASE 
        WHEN description = 'inclusao de pagamento' THEN 0
        WHEN description LIKE '%pagamento%' THEN 0
        ELSE amount_brl 
    END) AS total_gasto_real,
    COUNT(CASE 
        WHEN description = 'inclusao de pagamento' THEN NULL
        ELSE 1 
    END) AS quantidade_transacoes
FROM analytics.fact_credit_card_statements
WHERE amount_brl > 0 OR description = 'estorno tarifa'  -- mantém estorno de tarifa
GROUP BY DATE_TRUNC('month', purchased_at)
ORDER BY mes DESC;

-- Ver todas as transações de abril com seus valores brutos135533
SELECT 
    purchased_at,
    description,
    amount_brl,
    CASE 
        WHEN amount_brl < 0 THEN 'CREDITO'
        ELSE 'DEBITO'
    END AS tipo
FROM analytics.fact_credit_card_statements
WHERE purchased_at >= '2026-04-01' 
  AND purchased_at < '2026-05-01'
ORDER BY purchased_at;

SELECT 
    TO_CHAR(DATE_TRUNC('month', purchased_at), 'YYYY-MM') AS mes,
    -- Soma total (convertendo para numeric para evitar imprecisão de double precision)
    ROUND(CAST(SUM(ABS(amount_brl)) AS NUMERIC), 2) AS total_gasto_geral,
    
    -- Divisão por método para conferência
    ROUND(CAST(SUM(CASE WHEN payment_type = 'credit_card' THEN ABS(amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_cartao,
    ROUND(CAST(SUM(CASE WHEN payment_type = 'pix' THEN ABS(amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_pix,
    
    COUNT(*) AS quantidade_transacoes
FROM analytics.fact_unified_payments
-- Filtro essencial para não contar o pagamento da fatura como um gasto novo
WHERE description NOT ILIKE '%pagamento%' 
  AND description NOT ILIKE '%inclusao de pagamento%'
GROUP BY 1
ORDER BY 1 DESC;

SELECT 
    -- Mudamos para invoice_name para bater com o valor real do boleto pago
    COALESCE(invoice_name, TO_CHAR(purchased_at, 'YYYY-MM')) AS competencia,
    
    -- Total do Cartão (agora considerando o ciclo da fatura)
    ROUND(CAST(SUM(CASE WHEN payment_type = 'credit_card' THEN ABS(amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_cartao_fatura,
    
    -- Total do PIX (limpando pagamentos de fatura e transferências)
    ROUND(CAST(SUM(CASE WHEN payment_type = 'pix' THEN ABS(amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_pix_puro,
    
    ROUND(CAST(SUM(ABS(amount_brl)) AS NUMERIC), 2) AS total_consumo_real
FROM analytics.fact_unified_payments
WHERE 
    -- Filtros mais agressivos para limpar pagamentos de fatura do PIX
    description NOT ILIKE '%pagamento%' 
    AND description NOT ILIKE '%inclusao%'
    AND description NOT ILIKE '%fatura%'  -- Isso remove o "Fatura - Cartão de crédito C6"
    AND description NOT ILIKE '%c6 bank%' -- Remove transferências entre suas contas se houver
GROUP BY 1
ORDER BY 1 DESC;


WITH card_invoices AS (
    -- Pegamos a informação de fatura direto da fonte onde ela existe
    SELECT 
        payment_id, 
        invoice_name 
    FROM analytics.fact_credit_card_statements
)

SELECT 
    -- Se for cartão, usamos a fatura. Se for PIX, usamos o mês da compra.
    COALESCE(ci.invoice_name, TO_CHAR(f.purchased_at, 'YYYY-MM')) AS competencia,
    
    -- Valor do Cartão (Agrupado por Fatura)
    ROUND(CAST(SUM(CASE WHEN f.payment_type = 'credit_card' THEN ABS(f.amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_cartao_fatura,
    
    -- Valor do PIX (Limpando os pagamentos de fatura que você mencionou)
    ROUND(CAST(SUM(CASE WHEN f.payment_type = 'pix' THEN ABS(f.amount_brl) ELSE 0 END) AS NUMERIC), 2) AS total_pix_limpo,
    
    ROUND(CAST(SUM(ABS(f.amount_brl)) AS NUMERIC), 2) AS total_geral
FROM analytics.fact_unified_payments f
LEFT JOIN card_invoices ci ON f.payment_id = ci.payment_id
WHERE 
    f.description NOT ILIKE '%pagamento%' 
    AND f.description NOT ILIKE '%inclusao%'
    AND f.description NOT ILIKE '%fatura%'  -- Remove "Fatura - Cartão de crédito C6"
    AND f.description NOT ILIKE '%c6 bank%' -- Limpa transferências internas
GROUP BY 1
ORDER BY 1 DESC;

SELECT description, amount_brl 
FROM analytics.fact_unified_payments 
WHERE invoice_name LIKE '%2026-04%' 
  AND payment_type = 'credit_card'
ORDER BY amount_brl ASC; -- Os créditos aparecerão primeiro



SELECT description, amount_brl, invoice_name
FROM analytics.fact_unified_payments
WHERE invoice_name LIKE 'Fatura_2026-05%'
  AND (
     description ILIKE '%pagamento%' 
     OR description ILIKE '%inclusao%'
     OR description ILIKE '%fatura%'
     OR description ILIKE '%c6 bank%'
     OR description ILIKE '%transferencia enviada%'
  );


select
    sum(amount_brl) as soma
From analytics.fact_credit_card_statements
where invoice_name = 'Fatura_2026-05-05.csv';

select * from analytics.fact_credit_card_statements
where invoice_name = 'Fatura_2026-05-05.csv';

select * from analytics.fact_credit_card_statements;

SELECT 
    CASE 
        WHEN invoice_name LIKE 'Fatura_%' THEN SUBSTRING(invoice_name FROM 8 FOR 7)
        ELSE TO_CHAR(purchased_at, 'YYYY-MM') 
    END AS competencia,
    
    ROUND(CAST(SUM(
        CASE 
            WHEN payment_type = 'credit_card' THEN amount_brl 
            ELSE 0 
        END
    ) AS NUMERIC), 2) AS total_cartao,
    
    ROUND(CAST(SUM(
        CASE 
            WHEN payment_type = 'pix' THEN amount_brl 
            ELSE 0 
        END
    ) AS NUMERIC), 2) AS total_pix,
    
    ROUND(CAST(SUM(amount_brl) AS NUMERIC), 2) AS total_geral
FROM analytics.fact_unified_payments
WHERE 
    -- 1. Mantemos apenas o que é gasto real ou estorno de loja
    -- Baseado no seu print, pagamentos de fatura não possuem categoria preenchida
    final_category IS NOT NULL 
    AND final_category <> '-'
    AND final_category <> ''
    
    -- 2. Filtros de segurança para transferências bancárias que possam ter categoria
    AND description NOT ILIKE '%c6 bank%'
    AND description NOT ILIKE '%transferencia enviada%'
    
    -- 3. Exceção específica para a Natura (caso ela venha sem categoria por algum motivo)
    OR (description ILIKE '%natura%' AND payment_type = 'credit_card')

GROUP BY 1
ORDER BY 1 DESC;


-- Querie to know all the credit card invoices
SELECT 
    CASE 
        WHEN invoice_name LIKE 'Fatura_%' THEN SUBSTRING(invoice_name FROM 8 FOR 7)
        ELSE TO_CHAR(purchased_at, 'YYYY-MM') 
    END AS competencia,
    ROUND(SUM(amount_brl)::NUMERIC, 2) AS total_fatura,
    COUNT(*) AS qtd_transacoes,
    -- Validação: Se o total for negativo, ainda tem pagamento de fatura "vazando"
    CASE WHEN SUM(amount_brl) < 0 THEN '❌ REVISAR: Valor Negativo' ELSE '✅ OK' END as status
FROM analytics.fct_credit_card_statements -- Use o nome da tabela que o dbt criou
GROUP BY 1
ORDER BY 1 DESC;

-- To know the total amount of an expecific month,
  SELECT 
    SUM(valor) as total_bruto_maio,
    SUM(CASE 
        WHEN lower(descricao) ilike '%fatura%' THEN valor 
        WHEN lower(descricao) ilike '%c6 bank%' THEN valor 
        WHEN upper(categoria) = 'PAGAMENTOS' AND upper(subcategoria) = 'CARTÃO DE CRÉDITO' THEN valor
        ELSE 0 
    END) as total_que_o_dbt_esta_tirando,
    SUM(CASE 
        WHEN NOT (lower(descricao) ilike '%fatura%' 
             OR lower(descricao) ilike '%c6 bank%' 
             OR (upper(categoria) = 'PAGAMENTOS' AND upper(subcategoria) = 'CARTÃO DE CRÉDITO')) 
        THEN valor 
        ELSE 0 
    END) as total_que_deveria_ir_para_fact
FROM postgres_raw.payment_pix
WHERE data_compra >= '2026-05-01' AND data_compra <= '2026-05-31';


-- Total expenses value (monthly)
SELECT 
    -- Agrupamento por mês/ano (Competência)
    CASE 
        WHEN invoice_name LIKE 'Fatura_%' THEN SUBSTRING(invoice_name FROM 8 FOR 7)
        ELSE TO_CHAR(purchased_at, 'YYYY-MM') 
    END AS competencia,
    
    -- Soma de Cartão de Crédito
    ROUND(SUM(CASE WHEN payment_type = 'credit_card' THEN amount_brl ELSE 0 END)::NUMERIC, 2) AS gasto_cartao,
    
    -- Soma de PIX (Já limpo de transferências internas e faturas)
    ROUND(SUM(CASE WHEN payment_type = 'pix' THEN amount_brl ELSE 0 END)::NUMERIC, 2) AS gasto_pix,
    
    -- Consolidado Total
    ROUND(SUM(amount_brl)::NUMERIC, 2) AS total_consumo_mes,
    
    -- Contador de transações para conferência
    COUNT(*) AS total_transacoes
FROM analytics.fct_unified_payments
-- Garante que só pegamos o que é gasto real (filtros do dbt)
WHERE is_internal_transfer = FALSE 
  AND is_payment_transaction = FALSE
GROUP BY 1
ORDER BY 1 DESC;

select * from analytics.fct_investments;
