CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    data_compra TIMESTAMP,
    estabelecimento TEXT,
    tipo_estabelecimento TEXT, -- 'Mercado' ou 'Restaurante'
    produto_codigo TEXT,
    descricao TEXT,
    categoria TEXT,
    quantidade NUMERIC(10,3),
    unidade TEXT,
    preco_unitario_bruto NUMERIC(10,2),
    desconto_item NUMERIC(10,2) DEFAULT 0,
    valor_total_final NUMERIC(10,2)
);