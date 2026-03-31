TRUNCATE TABLE fact_market_items;

-- Inserindo o Mercado
INSERT INTO dim_market (name, location, city) 
VALUES ('Tauste', 'Vila America', 'Bauru');

-- Inserindo os Produtos Únicos (Baseado no seu cupom)
INSERT INTO dim_product (product_code, description, category, subcategory) VALUES
('7622210568601', 'BOMBOM LACTA SONHO DE VALSA', 'Mercearia', 'Doces/Chocolates'),
('7891172433078', 'PAP HIG NEVE FD 30 NEU', 'Higiene', 'Papelaria/Banho'),
('7891150086531', 'DET PO BRILHANTE LIM', 'Limpeza', 'Lavanderia'),
('20725', 'CX ASA FRANGO', 'Açougue', 'Aves'),
('15356', 'PANCETA SUINA', 'Açougue', 'Suínos'),
('3292', 'TOMATE ITALIANO', 'Hortifruti', 'Legumes'),
('3926', 'BANANA NANICA', 'Hortifruti', 'Frutas'),
('2981', 'ABOBORA CABOTIAN CUB', 'Hortifruti', 'Legumes'),
('21777', 'F FIGO STROGONOFF', 'Açougue', 'Bovinos'),
('3773', 'LIMAO TAITI', 'Hortifruti', 'Frutas'),
('7896945801047', 'OVO G VER OVOBOM 10B', 'Mercearia', 'Ovos'),
('9119', 'CEBOLA', 'Hortifruti', 'Legumes'),
('7891999011039', 'MARG VIGOR MANT C/S', 'Laticínios', 'Margarinas'),
('7898270967344', 'MOL SOJA KARUI LIGHT', 'Mercearia', 'Molhos/Condimentos'),
('3797', 'LARANJA', 'Hortifruti', 'Frutas'),
('7891527062991', 'FILE TILAPIA COPACOL', 'Peixaria', 'Peixes Congelados'),
('7891097101984', 'LEITE F BOB ESPONJA', 'Laticínios', 'Leite Infantil'),
('7898080640611', 'LEITE LV ITALAC INT', 'Laticínios', 'Leites'),
('7896275970857', 'D LEITE FRIMESA', 'Laticínios', 'Leite em Pó'),
('7898930142654', 'MOL TOM SALSAR RET', 'Mercearia', 'Molhos/Condimentos'),
('7891150042131', 'AMAC CONFORT I P CUI', 'Limpeza', 'Lavanderia')
ON CONFLICT (product_code) DO NOTHING;

INSERT INTO fact_market_items 
(transaction_date, market_id, product_code, quantity, unit_measure, unit_price_raw, discount_item, total_price_final) 
VALUES
('2026-03-30 08:22:14', 1, '7622210568601', 1, 'CX', 10.99, 0, 10.99),
('2026-03-30 08:22:14', 1, '7622210568601', 1, 'CX', 10.99, 0, 10.99),
('2026-03-30 08:22:14', 1, '7891172433078', 1, 'PC', 47.69, 0, 47.69),
('2026-03-30 08:22:14', 1, '7891150086531', 1, 'CX', 19.85, 0, 19.85),
('2026-03-30 08:22:14', 1, '20725', 1.052, 'KG', 11.98, 0, 12.60),
('2026-03-30 08:22:14', 1, '15356', 0.852, 'KG', 29.89, 0, 25.47),
('2026-03-30 08:22:14', 1, '3292', 0.735, 'KG', 10.75, 0, 7.90),
('2026-03-30 08:22:14', 1, '3926', 1.400, 'KG', 6.85, 0, 9.59),
('2026-03-30 08:22:14', 1, '2981', 0.408, 'KG', 12.97, 0, 5.29),
('2026-03-30 08:22:14', 1, '21777', 1.020, 'KG', 26.15, 0, 26.67),
('2026-03-30 08:22:14', 1, '3773', 0.655, 'KG', 2.95, 0, 1.93),
('2026-03-30 08:22:14', 1, '7896945801047', 1, 'BJ', 11.90, 0, 11.90),
('2026-03-30 08:22:14', 1, '9119', 0.725, 'KG', 4.95, 0, 3.59),
('2026-03-30 08:22:14', 1, '7891999011039', 1, 'PO', 9.79, 0, 9.79),
('2026-03-30 08:22:14', 1, '7898270967344', 1, 'PT', 21.49, 0, 21.49),
('2026-03-30 08:22:14', 1, '3797', 1.045, 'KG', 4.99, 0, 5.21),
('2026-03-30 08:22:14', 1, '7891527062991', 1, 'PC', 41.80, 0, 41.80),
('2026-03-30 08:22:14', 1, '7891097101984', 1, 'CJ', 7.58, 0.42, 7.16),
('2026-03-30 08:22:14', 1, '7891097101984', 1, 'CJ', 7.58, 0.42, 7.16),
('2026-03-30 08:22:14', 1, '7891097101984', 1, 'CJ', 7.58, 0.42, 7.16),
('2026-03-30 08:22:14', 1, '7898080640611', 1, 'TP', 5.45, 0, 5.45),
('2026-03-30 08:22:14', 1, '7896275970857', 1, 'PO', 11.49, 0, 11.49),
('2026-03-30 08:22:14', 1, '7898930142654', 1, 'SH', 2.15, 0, 2.15),
('2026-03-30 08:22:14', 1, '7891150042131', 1, 'FR', 18.90, 0, 18.90);