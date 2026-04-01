DROP TABLE IF EXISTS fact_investments;

CREATE TABLE fact_investments (
    id SERIAL PRIMARY KEY,
    owner TEXT,
    transaction_type TEXT, -- Substituiu 'order'
    transaction_date DATE,
    ticker TEXT,
    organization TEXT,
    asset_type TEXT, 
    quantity NUMERIC,
    unit_price NUMERIC,
    total_amount NUMERIC,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE fact_investments DROP COLUMN IF EXISTS cnpj;

DROP TABLE IF EXISTS dim_assets;

CREATE TABLE dim_assets (
    ticker TEXT PRIMARY KEY,
    company_name TEXT,
    cnpj TEXT,
    sector TEXT
);

