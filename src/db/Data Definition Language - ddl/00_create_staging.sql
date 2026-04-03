-- 1. Staging para o Excel de Outflow (Pix/Cash)
CREATE TABLE stg_outflow (
    transaction_date TEXT, -- Mantemos TEXT para o Python inserir rápido, convertemos na Fact
    week_day TEXT,
    description TEXT,
    amount NUMERIC(10,2),
    status TEXT,
    installment TEXT,
    notes TEXT,
    payment_method TEXT,
    payee_document TEXT,
    income_tax_applicable TEXT, -- 'Yes'/'No' vindo da planilha
    ingestion_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Staging para o CSV do Cartão de Crédito
-- Note que aqui as colunas espelham o CSV bruto para facilitar o LOAD
CREATE TABLE stg_credit_card_raw (
    purchase_date TEXT,
    card_name TEXT,
    card_last_digits TEXT,
    raw_category_description TEXT, -- O campo misto "Restaurante;NOME_LOJA"
    installment TEXT,
    amount_usd NUMERIC(10,2),
    exchange_rate NUMERIC(10,2),
    amount_brl NUMERIC(10,2),
    ingestion_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);