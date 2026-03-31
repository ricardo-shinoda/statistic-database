DROP TABLE IF EXISTS fact_market_items;

-- 1. Tabela de Mercados (Dimensão)
CREATE TABLE dim_market (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    city TEXT DEFAULT 'Bauru'
);

-- 2. Tabela de Produtos (Dimensão)
-- O product_code (EAN) é a nossa chave natural aqui
CREATE TABLE dim_product (
    product_code TEXT PRIMARY KEY,
    description TEXT,
    category TEXT,
    subcategory TEXT
);

-- 3. Tabela de Itens (Fato)
CREATE TABLE fact_market_items (
    id SERIAL PRIMARY KEY,
    transaction_date TIMESTAMP,
    market_id INTEGER REFERENCES dim_market(id),
    product_code TEXT REFERENCES dim_product(product_code),
    quantity NUMERIC(10,3),
    unit_measure TEXT,
    unit_price_raw NUMERIC(10,2),
    discount_item NUMERIC(10,2) DEFAULT 0,
    total_price_final NUMERIC(10,2)
);

