
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