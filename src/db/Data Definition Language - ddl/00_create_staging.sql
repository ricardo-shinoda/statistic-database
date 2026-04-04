
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