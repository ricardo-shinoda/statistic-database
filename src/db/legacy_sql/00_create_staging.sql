
-- 1. Limpeza Total
DROP TABLE IF EXISTS stg_excel_outflow;
DROP TABLE IF EXISTS stg_credit_card;
DROP TABLE IF EXISTS fact_transactions;

-- 2. Staging Excel (Baseado na aba 'pagamento' da imagem 3096fc)
CREATE TABLE stg_excel_outflow (
    data_compra DATE,
    descricao TEXT,
    valor NUMERIC(15,2),
    status_pagamento TEXT,
    parcela TEXT,
    metodo_pagamento TEXT,
    origem_arquivo TEXT,
    inserido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Staging CSV (Baseado na imagem 3099e7)
CREATE TABLE stg_credit_card (
    data_compra DATE,
    cartao_titular TEXT,
    categoria TEXT,
    descricao TEXT,
    parcela TEXT,
    valor NUMERIC(15,2),
    origem_arquivo TEXT,
    inserido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela Fato (O Coração do Projeto)
CREATE TABLE fact_transactions (
    id SERIAL PRIMARY KEY,
    data_compra DATE NOT NULL,
    descricao TEXT NOT NULL,
    valor NUMERIC(15,2) NOT NULL,
    parcela TEXT,
    status_pagamento TEXT,
    metodo_pagamento TEXT,
    categoria TEXT,
    cartao_titular TEXT,
    origem_pagamento TEXT, -- 'excel' ou 'credit_card'
    arquivo_origem TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- nova estrutura a partir daqui

CREATE TABLE pagamento_dinheiro (
    id SERIAL PRIMARY KEY,
    data_compra DATE NOT NULL,
    descricao TEXT NOT NULL,
    valor NUMERIC(15,2) NOT NULL,
    status_pagamento TEXT,  -- 'paid', 'pending', etc.
    parcela TEXT,           -- Ex: '1-4', '1-1'
    metodo_pagamento TEXT,  -- 'Cheque', 'Pix', 'Dinheiro'
    categoria TEXT,         -- Sugestão: Para facilitar o JOIN futuro
    comentario TEXT,
    arquivo_origem TEXT,    -- Para auditoria (Controle.xlsx)
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pagamento_cartao (
    id SERIAL PRIMARY KEY,
    data_compra DATE NOT NULL,
    cartao_titular TEXT,    -- 'RICARDO SHINODA'
    cartao_final TEXT,      -- Ex: '5439'
    categoria TEXT,         -- 'Supermercados', 'Transporte', etc.
    descricao TEXT,         -- 'DescriÃ§Ã£o' corrigida
    parcela TEXT,           -- '3/3' ou 'Ãšnica' (corrigir para 'Única')
    valor_usd NUMERIC(15,2),
    valor_brl NUMERIC(15,2) NOT NULL, -- 'Valor (em R$)'
    arquivo_origem TEXT,    -- Ex: 'invoice-2026-04.csv'
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drop existing table and recreate with all columns including comentario
DROP TABLE IF EXISTS pagamento_dinheiro CASCADE;

-- Drop existing table if it exists
DROP TABLE IF EXISTS pagamento_dinheiro CASCADE;

-- Create table with specified column order
CREATE TABLE pagamento_dinheiro (
    id SERIAL PRIMARY KEY,
    data_compra DATE,
    descricao VARCHAR(255),
    valor DECIMAL(10,2),
    status_pagamento VARCHAR(50),
    parcela VARCHAR(20),
    comentario TEXT,
    categoria VARCHAR(100),
    subcategoria VARCHAR(100),
    metodo_pagamento VARCHAR(50),
    arquivo_origem VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_pagamento_dinheiro_data_compra ON pagamento_dinheiro(data_compra);
CREATE INDEX idx_pagamento_dinheiro_categoria ON pagamento_dinheiro(categoria);
CREATE INDEX idx_pagamento_dinheiro_subcategoria ON pagamento_dinheiro(subcategoria);
CREATE INDEX idx_pagamento_dinheiro_comentario ON pagamento_dinheiro(comentario);