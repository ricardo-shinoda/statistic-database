-- Run this in SQLTools/VS Code first!
CREATE TABLE IF NOT EXISTS dim_merchant_mapping (
    original_description TEXT PRIMARY KEY,
    mapped_category TEXT NOT NULL,
    mapped_subcategory TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    amount_brl NUMERIC(15, 2) NOT NULL,
    card_holder_name TEXT,     
    installment_info TEXT,     -- e.g., '1/4'
    transaction_type TEXT,      -- 'credit_card' or 'manual_bill'
    status TEXT,               
    source_file TEXT,          
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE fact_transactions ADD COLUMN IF NOT EXISTS installment_info TEXT;

ALTER TABLE fact_transactions 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

DROP TABLE IF EXISTS fact_investments;

CREATE TABLE fact_investments (
    id SERIAL PRIMARY KEY,
    owner TEXT,
    transaction_type TEXT, -- Substituiu 'order'
    transaction_date DATE,
    ticker TEXT,
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

INSERT INTO dim_assets (ticker, company_name, cnpj, sector) VALUES
('BBSE3', 'BB Seguridade', '17.344.597/0001-94', 'Seguros'),
('ITSA4', 'Itaúsa', '61.532.644/0001-15', 'Holding Bancária'),
('PETR4', 'Petrobras', '33.000.167/0001-01', 'Petróleo e Gás'),
('SNAG11', 'Suno Agro', '28.152.777/0001-90', 'Agronegócio'),
('BBAS3', 'Banco do Brasil', '00.000.000/0001-91', 'Bancário'),
('KLBN4', 'Klabin', '89.637.490/0001-45', 'Papel e Celulose'),
('MALL11', 'Malls Brasil Plural', '28.152.777/0001-90', 'Imobiliário (Shoppings)'),
('RBRP11', 'RBR Properties', '28.152.777/0001-90', 'Imobiliário (Lajes)');