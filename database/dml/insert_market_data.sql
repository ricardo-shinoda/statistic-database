TRUNCATE TABLE purchases;

INSERT INTO postgres_raw.purchases 
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


INSERT INTO postgres_raw.purchases 
(data_compra, estabelecimento, tipo_estabelecimento, produto_codigo, descricao, categoria, quantidade, unidade, preco_unitario_bruto, desconto_item, valor_total_final)
VALUES
-- ==========================================
-- COMPRA COMPLETA (25/04/2026) - Tauste
-- ==========================================
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896623100714', 'SUCO XANDO LARANJA', 'Bebidas', 1, 'FR', 25.78, 1.42, 24.36),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896623100714', 'SUCO XANDO LARANJA', 'Bebidas', 1, 'FR', 25.78, 1.42, 24.36),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896602601315', 'ARROZ INARI T1 LON', 'Mercearia', 1, 'PC', 38.65, 0, 38.65),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891150086531', 'DET PO BRILHANTE LIM', 'Limpeza', 1, 'CX', 19.90, 0, 19.90),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900702217', 'REF COCA COLA S/ACU', 'Bebidas', 1, 'FD', 22.68, 0, 22.68),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891098041630', 'CHA LEÃO ICE LIM C/G', 'Bebidas', 6, 'LT', 4.39, 2.40, 23.94),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900360042', 'AGUA TON SCHUEPPES Z', 'Bebidas', 1, 'FD', 19.74, 0, 19.74),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900521504', 'AGUA S CRYSTAL FR U', 'Bebidas', 1, 'PT', 2.79, 0.30, 2.49),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900521504', 'AGUA S CRYSTAL FR U', 'Bebidas', 1, 'PT', 2.79, 0.30, 2.49),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900521009', 'AGUA S CRYSTAL TANG', 'Bebidas', 1, 'PT', 2.79, 0.30, 2.49),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900521009', 'AGUA S CRYSTAL MELAN', 'Bebidas', 1, 'PT', 2.79, 0.30, 2.49),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7894900521009', 'AGUA S CRYSTAL TANG', 'Bebidas', 1, 'PT', 2.79, 0.30, 2.49),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7892408220400', 'BAT RUFFLES ORI TUBO', 'Salgadinhos', 1, 'PQ', 10.99, 0, 10.99),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891203020260', 'PAO MEL PANCO CHOC', 'Doces', 1, 'PC', 9.79, 0, 9.79),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896618520859', 'LOMBO C CERATTI', 'Frios', 1, 'UN', 8.98, 0, 8.98),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '45681', 'QJO MUSSAREL FAT EMB', 'Frios', 0.236, 'KG', 49.90, 0, 11.78),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '789080371214', 'OUQ CAIP DIQUO', 'Mercearia', 1, 'BJ', 14.90, 0, 14.90),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '789080371214', 'OUQ CAIP DIQUO', 'Mercearia', 1, 'BJ', 14.90, 0, 14.90),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896304000012', 'MACA T DA HONICA', 'Hortifruti', 1, 'PC', 15.95, 0, 15.95),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAOU NAT I CRE', 'Laticínios', 1, 'PQ', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAOU NAT I CRE', 'Laticínios', 1, 'PQ', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAOU NAT I CRE', 'Laticínios', 1, 'PQ', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAOU NAT I CRE', 'Laticínios', 1, 'PQ', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '789100126905', 'CR LEITE NESTLE LEVE', 'Laticínios', 1, 'TP', 3.99, 0, 3.99),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '789100065440', 'LEITE COND MOÇA SEM', 'Doces', 1, 'TP', 7.70, 0, 7.70),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896552906869', 'COCO RAL COCONUT ADO', 'Mercearia', 1, 'PC', 4.39, 0, 4.39),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7695521906589', 'ARAHA FORTE', 'Bebidas', 0.525, 'KG', 7.65, 0, 4.02),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7622210533289', 'SN CLUB S PARMESAO', 'Salgadinhos', 1, 'PC', 8.45, 0, 8.45),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891999904805', 'LEITE F VIJOR', 'Laticínios', 1, 'CJ', 5.75, 0, 5.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0, 3.95),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0, 3.95),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7896074606919', 'PAO QJO F MINAS AIR', 'Padaria', 1, 'PC', 17.99, 0, 17.99),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '3254', 'BANANA PRATA', 'Hortifruti', 1.220, 'KG', 8.97, 0, 10.94),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891000358887', 'CH NESTLE CLAS AHEND', 'Doces', 1, 'BR', 12.90, 0, 12.90),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7891000358887', 'CH NESTLE CLAS AHEND', 'Doces', 2, 'BR', 12.90, 0, 12.90),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7897517209544', 'MILHO VERDE FUGINI', 'Mercearia', 1, 'SH', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7897517209544', 'MILHO VERDE FUGINI', 'Mercearia', 1, 'SH', 2.75, 0, 2.75),
('2026-04-25 16:02:48', 'Tauste', 'Mercado', '7898024395416', 'CH KINDER OVO PERSON', 'Doces', 1, 'CX', 12.98, 0, 12.98);

INSERT INTO postgres_raw.purchases 
(data_compra, estabelecimento, tipo_estabelecimento, produto_codigo, descricao, categoria, quantidade, unidade, preco_unitario_bruto, desconto_item, valor_total_final)
VALUES
-- ==========================================
-- COMPRA COMPLETA (02/05/2026) - Tauste
-- ==========================================
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898941331092', 'DES KIMAX MARINE', 'Limpeza', 1, 'FR', 5.98, 0, 5.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891150065154', 'AMAC COMFORT I P CUI', 'Limpeza', 1, 'FR', 24.87, 0, 24.87),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891035115608', 'LIMP DESTAC U O MAD', 'Limpeza', 1, 'FR', 18.70, 0, 18.70),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7892840824907', 'BAT LAYS QJO CAMEMB', 'Salgadinhos', 1, 'PC', 8.99, 0, 8.99),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7892840824884', 'BAT LAYS PICANHA BRA', 'Salgadinhos', 1, 'PC', 8.99, 0, 8.99),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898944856790', 'ALC DES SAFRA MARIN', 'Limpeza', 1, 'FR', 10.98, 1.00, 9.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891150044654', 'SAB DOVE KARITE/BAUN', 'Higiene', 1, 'CJ', 27.47, 0, 27.47),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7894930020046', 'REF SCHWEPPES CIT', 'Bebidas', 1, 'CX', 21.54, 0, 21.54),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7896045506873', 'CUJ HEINEKEN', 'Bebidas', 1, 'LT', 4.99, 0, 4.99),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7896045506873', 'CUJ HEINEKEN', 'Bebidas', 1, 'LT', 4.99, 0, 4.99),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7894900521009', 'AGUA S CRYSTAL TANG', 'Bebidas', 6, 'PT', 2.79, 1.80, 14.94),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '78969045102440', 'CAFE 3 COR TRAD VACU', 'Mercearia', 1, 'PC', 26.90, 0, 26.90),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '789107101984', 'LEITE F BOB ESPONJA', 'Laticínios', 1, 'CJ', 6.97, 0.38, 6.59),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891097101984', 'LEITE F BOB ESPONJA', 'Laticínios', 1, 'CJ', 6.97, 0.38, 6.59),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '2523', 'MANGA PALMER', 'Hortifruti', 1.080, 'KG', 7.95, 0, 7.95),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7894650014110', 'LIMP MR MUSC COZ', 'Limpeza', 1, 'SH', 11.95, 0, 11.95),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891000412855', 'ACHO NESCAM F CRESC', 'Mercearia', 1, 'LT', 8.98, 0, 8.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '3254', 'BANANA PRATA', 'Hortifruti', 0.820, 'KG', 8.97, 0, 8.97),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '3254', 'BANANA PRATA', 'Hortifruti', 0.565, 'KG', 8.97, 0, 8.97),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898930142654', 'MOL TOM SALSARET TRA', 'Mercearia', 1, 'SH', 1.49, 0, 1.49),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898924049051', 'QJO RAL RELIQUIA S', 'Frios', 1, 'PC', 5.89, 0, 5.89),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7899120500608', 'MILHO VERDE QUERO', 'Mercearia', 1, 'LT', 3.59, 0, 3.59),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '40259', 'QJO MUSSAREL GRANEL', 'Frios', 0.304, 'KG', 55.90, 0, 55.90),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0.60, 3.35),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0.60, 3.35),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0.60, 3.35),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891156020218', 'SUCO YAKULT MACA', 'Bebidas', 1, 'TP', 3.95, 0.60, 3.35),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891120302060', 'PAO MEL PANCO CHOC', 'Doces', 1, 'PC', 11.98, 0, 11.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '43847', 'LING C AURORA GRA', 'Açougue', 0.376, 'KG', 24.99, 0, 9.40),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '2073', 'ABOB ITALIA VACUO', 'Hortifruti', 0.410, 'KG', 15.95, 0, 6.54),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '3841', 'CENOURA', 'Hortifruti', 0.450, 'KG', 9.98, 0, 4.49),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898453418410', 'ALHO PO BOMBAY', 'Mercearia', 1, 'PC', 11.95, 0, 11.95),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7897721410095', 'MAC PETYBON OU PENA', 'Petshop', 1, 'PC', 3.49, 0, 3.49),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAVO NAT 1 CRE', 'Laticínios', 1, 'PO', 3.69, 0, 3.69),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAVO NAT 1 CRE', 'Laticínios', 1, 'PO', 3.69, 0, 3.69),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAVO NAT I CRE', 'Laticínios', 1, 'PO', 3.69, 0, 3.69),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891097104190', 'IOG BATAVO NAT 1 CRE', 'Laticínios', 1, 'PO', 3.69, 0, 3.69),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7861002901855', 'PAST TIC TAC LARANJA', 'Doces', 1, 'FR', 9.98, 0, 9.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891000359006', 'CH NESTLE CLAS DUO C', 'Doces', 1, 'BR', 12.98, 0, 12.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7891000358887', 'CH NESTLE CLAS AMEND', 'Doces', 1, 'BR', 12.98, 0, 12.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '32360', 'PAO DA VOVU', 'Padaria', 0.368, 'KG', 34.90, 0, 12.84),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7896074606919', 'PAO QJO F MINAS AIR', 'Padaria', 1, 'PC', 17.90, 0, 17.90),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7898096453809', 'SALADA CEN/BET CAISP', 'Hortifruti', 1, 'PO', 11.98, 0, 11.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '3193', 'CAQUI RAMA FORTE', 'Hortifruti', 0.935, 'KG', 7.65, 0, 7.15),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7896001003323', 'SC LIXO ESFREBOM 50L', 'Limpeza', 1, 'PC', 15.99, 0, 15.99),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '7896353301634', 'REQ CATUPIRY ERVAS F', 'Laticínios', 1, 'CP', 9.98, 0, 9.98),
('2026-05-02 09:39:55', 'Tauste', 'Mercado', '40232797668', 'CEBO LINHA PICADA', 'Hortifruti', 1, 'UN', 7.09, 0, 7.09);


-- 04-05 Padaria aviação 0527 R$ 42,40 - CAFÉ DA MANHÃ PAULA
-- 03/05 IFD*CAYO CARBONE TEIXE BAURU 6499 R$ 43,59 LANCHE
-- 03-05 PG*LI LOJA WALDORF 0350 R$134,70 - ESTOJO
-- 02/05 AMAZON BR 6499 R$89,80 - CREME HIDRATANTE


