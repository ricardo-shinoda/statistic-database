
CREATE TABLE IF NOT EXISTS postgres_raw.purchases (
    id SERIAL PRIMARY KEY,
    data_compra TIMESTAMP NOT NULL,
    estabelecimento TEXT,
    tipo_estabelecimento TEXT,
    produto_codigo TEXT,
    descricao TEXT NOT NULL,
    categoria TEXT,
    quantidade NUMERIC(10,3) NOT NULL,
    unidade TEXT,
    preco_unitario_bruto NUMERIC(10,2),
    desconto_item NUMERIC(10,2),
    valor_total_final NUMERIC(10,2),
    inserido_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evolução dos gastos por semana/mês
SELECT 
    DATE_TRUNC('month', data_compra) as mes,
    estabelecimento,
    SUM(valor_total_final) as total_mes,
    COUNT(DISTINCT data_compra) as qtd_compras,
    ROUND(AVG(valor_total_final), 2) as ticket_medio
FROM postgres_raw.purchases
GROUP BY mes, estabelecimento
ORDER BY mes DESC;

-- Query para dashboard/resumo executivo
SELECT 
    'Total Itens' as metrica, 
    COUNT(*)::text as valor 
FROM postgres_raw.purchases 
WHERE data_compra = '2026-05-02 09:39:55'
UNION ALL
SELECT 'Total Gasto', ROUND(SUM(valor_total_final)::numeric, 2)::text
FROM postgres_raw.purchases 
WHERE data_compra = '2026-05-02 09:39:55'
UNION ALL
SELECT 'Desconto Total', ROUND(SUM(desconto_item)::numeric, 2)::text
FROM postgres_raw.purchases 
WHERE data_compra = '2026-05-02 09:39:55'
UNION ALL
SELECT 'Ticket Medio', ROUND(AVG(valor_total_final)::numeric, 2)::text
FROM postgres_raw.purchases 
WHERE data_compra = '2026-05-02 09:39:55'
UNION ALL
SELECT 'Qtd Categorias', COUNT(DISTINCT categoria)::text
FROM postgres_raw.purchases 
WHERE data_compra = '2026-05-02 09:39:55';

-- Quanto gastou em cada categoria
SELECT 
    categoria,
    COUNT(*) as qtd_itens,
    SUM(quantidade) as quantidade_total,
    SUM(valor_total_final) as total_gasto,
    ROUND(AVG(preco_unitario_bruto), 2) as preco_medio
FROM postgres_raw.purchases
-- WHERE data_compra = '2026-05-02 09:39:55'
GROUP BY categoria
ORDER BY total_gasto DESC;