-- Limpa a tabela para garantir que não haja duplicatas antes de inserir a lista completa
TRUNCATE TABLE compras;

INSERT INTO compras 
(data_compra, estabelecimento, tipo_estabelecimento, produto_codigo, descricao, categoria, quantidade, unidade, preco_unitario_bruto, desconto_item, valor_total_final)
VALUES
-- ==========================================
-- COMPRA COMPLETA (30/03/2026) - Tauste
-- ==========================================
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7622210568601', 'BOMBOM LACTA SONHO DE VALSA', 'Doces', 2, 'CX', 10.99, 0, 21.98),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891172433078', 'PAP HIG NEVE FD 30 NEU', 'Higiene', 1, 'PC', 47.69, 0, 47.69),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891150086531', 'DET PO BRILHANTE LIM', 'Limpeza', 1, 'CX', 19.85, 0, 19.85),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '20725', 'CX ASA FRANGO', 'Açougue', 1.052, 'KG', 11.98, 0, 12.60),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '15356', 'PANCETA SUINA', 'Açougue', 0.852, 'KG', 29.89, 0, 25.47),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '3292', 'TOMATE ITALIANO', 'Hortifruti', 0.735, 'KG', 10.75, 0, 7.90),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '3926', 'BANANA NANICA', 'Hortifruti', 1.400, 'KG', 6.85, 0, 9.59),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '2981', 'ABOBORA CABOTIAN CUB', 'Hortifruti', 0.408, 'KG', 12.97, 0, 5.29),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '21777', 'F FIGO STROGONOFF', 'Açougue', 1.020, 'KG', 26.15, 0, 26.67),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '3773', 'LIMAO TAITI', 'Hortifruti', 0.655, 'KG', 2.95, 0, 1.93),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7896945801047', 'OVO G VER OVOBOM 10B', 'Mercearia', 1, 'BJ', 11.90, 0, 11.90),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '9119', 'CEBOLA', 'Hortifruti', 0.725, 'KG', 4.95, 0, 3.59),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891999011039', 'MARG VIGOR MANT C/S', 'Laticínios', 1, 'PO', 9.79, 0, 9.79),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7898270967344', 'MOL SOJA KARUI LIGHT', 'Mercearia', 1, 'PT', 21.49, 0, 21.49),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '3797', 'LARANJA', 'Hortifruti', 1.045, 'KG', 4.99, 0, 5.21),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891527062991', 'FILE TILAPIA COPACOL', 'Peixaria', 1, 'PC', 41.80, 0, 41.80),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891097101984', 'LEITE F BOB ESPONJA', 'Laticínios', 3, 'CJ', 7.58, 1.26, 21.48),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7898080640611', 'LEITE LV ITALAC INT', 'Laticínios', 1, 'TP', 5.45, 0, 5.45),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7896275970857', 'D LEITE FRIMESA', 'Laticínios', 1, 'PO', 11.49, 0, 11.49),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7898930142654', 'MOL TOM SALSAR RET', 'Mercearia', 1, 'SH', 2.15, 0, 2.15),
('2026-03-30 08:22:14', 'Tauste', 'Mercado', '7891150042131', 'AMAC CONFORT I P CUI', 'Limpeza', 1, 'FR', 18.90, 0, 18.90),

-- ==========================================
-- COMPRA RESTAURANTE (03/04/2026)
-- ==========================================
('2026-04-03 14:45:00', 'Consumer Restaurante', 'Restaurante', 'COPO-M', 'Copo M', 'Bebidas', 2, 'UN', 19.00, 0, 38.00),
('2026-04-03 14:45:00', 'Consumer Restaurante', 'Restaurante', 'ICHIGO-DAIFUKU', 'Ichigodaifuku', 'Sobremesa', 1, 'UN', 16.00, 0, 16.00),
('2026-04-03 14:45:00', 'Consumer Restaurante', 'Restaurante', 'MOCHI-MATCHY', 'Mochi com Sorvete Matcha', 'Sobremesa', 1, 'UN', 16.00, 0, 16.00),
('2026-04-03 14:45:00', 'Consumer Restaurante', 'Restaurante', 'COOKIE-OREO', 'Cookie do Mes - Oreo', 'Sobremesa', 1, 'UN', 17.50, 0, 17.50),

-- ==========================================
-- COMPRA HOJE (04/04/2026) - Tauste (Foto 1)
-- ==========================================

-- COMPRA TAUSTE COMPLETA (04/04/2026)
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7896132200011', 'MACA SENNINHA 1 PC', 'Hortifruti', 1, 'PC', 11.95, 0, 11.95),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7896009761911', 'PILHA RAYOVAC AAA 1 CT', 'Utilidades', 1, 'CT', 9.49, 0, 9.49),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '3841', 'CENOURA KG', 'Hortifruti', 0.470, 'KG', 6.98, 0, 3.28),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '2523', 'MANGA PALMER KG', 'Hortifruti', 0.845, 'KG', 5.95, 0, 5.03),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '3254', 'BANANA PRATA KG', 'Hortifruti', 0.610, 'KG', 8.97, 0, 5.47),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7898945024235', 'TOM DOCE GR B ORG 1 BJ', 'Hortifruti', 1, 'BJ', 5.95, 0, 5.95),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '2981', 'ABOBORA CABOTIAN CUB', 'Hortifruti', 0.456, 'KG', 12.97, 0, 5.91),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7622210533005', 'SN CLUB S CHURRAS 1 PC', 'Snacks', 1, 'PC', 6.45, 0, 6.45),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7622210574695', 'SN CLUB S PARMESAO 1 PC', 'Snacks', 1, 'PC', 6.45, 0, 6.45),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7897300506218', 'PA LIXO PLAST S FRAN 1 PE', 'Limpeza', 1, 'PE', 25.49, 0, 25.49),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '33640', 'BOLO PAO DE MEL FAT', 'Padaria', 0.528, 'KG', 39.90, 0, 21.07),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7896623100509', 'SUCO XANDO LARANJA 1 GF', 'Bebidas', 3, 'GF', 9.90, 1.62, 28.08),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891035116513', 'LIMP DESTAC P LAMIN 1 FR', 'Limpeza', 1, 'FR', 18.50, 2.51, 15.99),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891515551360', 'COUVE FLOR SADIA CG 1 PC', 'Congelados', 1, 'PC', 23.97, 0, 23.97),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891515551230', 'BROCOLIS SADIA CG 1 PC', 'Congelados', 1, 'PC', 19.67, 0, 19.67),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '45681', 'QJO MUSSAREL FAT EMB', 'Frios', 0.296, 'KG', 49.90, 0, 14.77),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891527062991', 'FILE TILAPIA COPACOL', 'Peixaria', 1, 'PC', 43.80, 0, 43.80),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7898921567916', 'BAT BEN BRASIL R ERV 1 PC', 'Congelados', 1, 'PC', 14.96, 0, 14.96),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7897517920036', 'FIO D KESS BASIC 1 PE', 'Higiene', 1, 'PE', 7.98, 0, 7.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA 1 TP', 'Bebidas', 3, 'TP', 2.95, 0, 8.85),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891097101984', 'LEITE F BOB ESPONJA 1 CJ', 'Bebidas', 2, 'CJ', 5.99, 0, 11.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891098041630', 'CHA LEAO ICE LIM C/G 6 LT', 'Bebidas', 6, 'LT', 4.39, 2.40, 23.94),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891000359006', 'CH NESTLE CLAS DUO 1 BR', 'Doces', 1, 'BR', 14.98, 0, 14.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7891000358887', 'CH NESTLE CLAS AMEND 1 BR', 'Doces', 1, 'BR', 14.98, 0, 14.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7898930142654', 'MOL TOM SALSARET TRA 1 SH', 'Mercearia', 2, 'SH', 2.28, 0, 4.56),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '789830672472', 'P AL WYDA 45X7,5 1 RL', 'Utilidades', 1, 'RL', 9.75, 0, 9.75),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '887961662351', 'P HOT WHEELS LAN C/C 1 PE', 'Brinquedos', 1, 'PE', 49.90, 0, 49.90),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7897721410095', 'MAC PETYBON OV PENA 1 PC', 'Mercearia', 1, 'PC', 3.49, 0, 3.49),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '789891637244', 'ALGODAO COTONDELA BO 1 PC', 'Higiene', 1, 'PC', 5.99, 0, 5.99),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7896045102440', 'CAFE 3 COR TRAD VACU 1 PC', 'Bebidas', 1, 'PC', 26.90, 0, 26.90),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7896045506873', 'CVJ HEINEKEN 1 LT', 'Bebidas', 3, 'LT', 4.99, 0, 14.97),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7894900520507', 'AGUA S CRYSTAL LIMAO 1 PT', 'Bebidas', 2, 'PT', 2.79, 0.60, 4.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7894900523003', 'AGUA S CRYSTAL MELAN 1 PT', 'Bebidas', 2, 'PT', 2.79, 0.60, 4.98),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7894650009055', 'P AD PATO FRESH 1 CX', 'Limpeza', 1, 'CX', 9.55, 0, 9.55),
('2026-04-04 10:42:37', 'Tauste', 'Mercado', '7897865300054', 'TEMP GABRIELA ALHO P 1 PO', 'Mercearia', 1, 'PO', 11.39, 0, 11.39);