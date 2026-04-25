# import pandas as pd
# from sqlalchemy import create_engine, text
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload
# import io
# import zipfile
# import os
# import re
# from dotenv import load_dotenv
# from pathlib import Path

# load_dotenv()

# # --- CONFIGURAÇÕES DO DRIVE ---
# SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# GOOGLE_DRIVE_INVOICE = os.getenv('GOOGLE_DRIVE_INVOICE')  # Pasta dos ZIPs
# GOOGLE_DRIVE_CONTROLE = os.getenv('GOOGLE_DRIVE_CONTROLE') # Pasta da Planilha Controle

# # --- CONFIGURAÇÕES DO BANCO ---
# # (Mantemos seu bloco de engine atual...)

# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASS')
# host = os.getenv('DB_HOST')
# port = os.getenv('DB_PORT')
# db_name = os.getenv('DB_NAME')
# raw_path = os.getenv('RAW_DATA_CREDIT_CARD')
# path_control = Path(os.getenv('RAW_DATA_CONTROLE', ''))
# path_pix = Path(os.getenv('RAW_DATA_PIX', ''))

# db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
# engine = create_engine(db_url)

# # --- FUNÇÕES DE APOIO ---
# def get_drive_service():
#     creds = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
#     return build('drive', 'v3', credentials=creds)

# def get_already_processed_files():
#     """Busca no banco quais faturas já foram inseridas para evitar duplicidade"""
#     try:
#         query = "SELECT DISTINCT arquivo_origem FROM postgres_raw.payment_card"
#         df = pd.read_sql(query, engine)
#         return df['arquivo_origem'].tolist()
#     except:
#         return []

# # --- FUNÇÃO MESTRE DE PROCESSAMENTO ---

# def process_everything_from_drive():
#     service = get_drive_service()
#     processados = get_already_processed_files()

#     # 1. BUSCAR E PROCESSAR A PLANILHA CONTROLE
#     # (Aqui buscamos o arquivo 'Controle.xlsx' no GOOGLE_DRIVE_CONTROLE)
#     # Rodamos as funções: process_pagamento_dinheiro, process_income, etc.
    
#     # 2. BUSCAR E PROCESSAR OS ZIPS DE FATURA
#     # (Aqui entramos na lógica do ZIP que conversamos)
#     # Se o CSV dentro do ZIP não estiver na lista 'processados', ele entra!

# # ... (Suas funções clean_currency e lógicas de aba continuam aqui)
# # 2. FUNÇÃO DE LIMPEZA MÍNIMA (Essencial para o Python não quebrar o Float)
# def clean_currency(series):
#     def clean_single_value(val):
#         if pd.isna(val) or val == '' or val == '-':
#             return 0.0
#         s = str(val).strip().replace('R$', '')
#         if ',' in s:
#             if '.' in s: s = s.replace('.', '').replace(',', '.')
#             else: s = s.replace(',', '.')
#         s = re.sub(r'[^0-9.-]', '', s)
#         try:
#             return float(s)
#         except ValueError:
#             return 0.0
#     return series.apply(clean_single_value)

# # 3. PROCESSAMENTO DE CARTÃO (Extract & Load)
# def process_pagamento_cartao():
#     if not raw_path:
#             print("⚠️ Variável RAW_DATA_CREDIT_CARD not defined on .env")
#     base_path = Path(raw_path)
#     files = list(base_path.rglob("*.csv"))
    
#     print(f"📂 Faturas encontradas: {len(files)}")
    
#     for csv_file in files:
#         try:
#             # Lê o CSV bruto
#             df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
#             df = df.dropna(how='all')

#             if not df.empty:
#                 # Adiciona apenas metadado de origem
#                 df['arquivo_origem'] = f"{csv_file.parent.name}/{csv_file.name}"
                
#                 # Garante que as colunas de valor sejam numéricas antes de subir
#                 # No dbt você usará o nome original da coluna (ex: "Valor (em R$)")
#                 for col in df.columns:
#                     if 'valor' in col.lower():
#                         df[col] = clean_currency(df[col])

#                 # Sobe para o schema postgres_raw
#                 df.to_sql('payment_card', engine, schema='postgres_raw', if_exists='append', index=False)
#                 print(f"   ✅ {csv_file.name} inserido.")
#         except Exception as e:
#             print(f"   ❌ Erro em {csv_file.name}: {e}")

# # 4. PROCESSAMENTO DE PIX/DINHEIRO (Extract & Load)
# def process_pagamento_dinheiro():
#     if not path_pix.exists():
#         print(f"⚠️ Arquivo {path_pix} não encontrado.")
#         return

#     # Lê a aba inteira. Se o dbt precisar de colunas novas, basta mudar o SQL lá.
#     df = pd.read_excel(path_pix, sheet_name='pagamento')
#     df = df.dropna(how='all')
    
#     # Limpeza básica de valor
#     for col in df.columns:
#         if 'valor' in col.lower():
#             df[col] = clean_currency(df[col])
            
#     df['arquivo_origem'] = 'Controle.xlsx'
    
#     # IMPORTANTE: Para o Pix, usamos 'replace' para garantir que a tabela reflita o Excel atual
#     df.to_sql('payment_pix', engine, schema='postgres_raw', if_exists='replace', index=False)
#     print(f"✅ {len(df)} registros de Pix enviados para postgres_raw.")

# # 5. PROCESS OF INCOME 
# def process_income():
#     # path_control = os.getenv('RAW_DATA_CONTROLE')
#     if not path_control.exists():
#         print(f"⚠️ File {path_control} not found.")
#         return
    
#     # Read the whole tab
#     df = pd.read_excel(path_control, sheet_name='entrada')
#     df = df.dropna(how='all')

#     # Value clean up

#     for col in df.columns:
#         if 'value' in col.lower():
#             df[col] = clean_currency(df[col])

#     df['arquivo_origem'] = 'Controle.xlsx'

#     # Use replace so the table will always show the latest Excel file
#     df.to_sql('income', engine, schema='postgres_raw', if_exists='replace', index=False)
#     print(f"✅ {len(df)} income data registered on postgres_raw.")


# def process_combustivel():
#     # path_control = os.getenv('RAW_DATA_CONTROLE')
#     # Carrega a aba de consumo do Nissan Kicks
#     df = pd.read_excel(path_control, sheet_name='nissan_kicks_consumption')
#     df = df.dropna(how='all')
    
#     # Limpeza básica de valores numéricos (se houver colunas de valor/litros)
#     for col in df.columns:
#         if any(keyword in col.lower() for keyword in ['valor', 'litro', 'km', 'preço']):
#             df[col] = clean_currency(df[col])
            
#     df['arquivo_origem'] = 'Controle.xlsx'
#     df.to_sql('nissan_kicks_consumption', engine, schema='postgres_raw', if_exists='replace', index=False)
#     print(f"✅ Aba de combustível carregada em postgres_raw.")

# def process_investimentos():
#     # path_control = os.getenv('RAW_DATA_CONTROLE')
#     # Carrega a aba de movimentos de estoque/ações
#     df = pd.read_excel(path_control, sheet_name='stock_movements')
#     df = df.dropna(how='all')
    
#     for col in df.columns:
#         if any(keyword in col.lower() for keyword in ['valor', 'preço', 'quantidade', 'taxa']):
#             df[col] = clean_currency(df[col])
            
#     df['arquivo_origem'] = 'Controle.xlsx'
#     df.to_sql('stock_movements', engine, schema='postgres_raw', if_exists='replace', index=False)
#     print(f"✅ Aba de investimentos carregada em postgres_raw.")

# # 5. EXECUÇÃO PRINCIPAL
# if __name__ == "__main__":
#     try:
#         with engine.connect() as conn:
#             print("🏗️ Preparando ambiente...")
#             # O CASCADE remove a tabela E as views do dbt que dependem dela temporariamente
#             conn.execute(text("DROP TABLE IF EXISTS postgres_raw.payment_card CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS postgres_raw.payment_pix CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS postgres_raw.nissan_kicks_consumption CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS postgres_raw.stock_movements CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS postgres_raw.income CASCADE;"))
            
#             conn.execute(text("CREATE SCHEMA IF NOT EXISTS postgres_raw;"))
#             conn.commit()
#             print("🧹 Tabelas antigas removidas com CASCADE.")
#     except Exception as e:
#         print(f"⚠️ Aviso na preparação: {e}")

#     # Agora as cargas vão funcionar porque o caminho está livre
#     process_pagamento_dinheiro()
#     process_pagamento_cartao()
#     process_combustivel()
#     process_investimentos()
#     process_income()

#     print("\n🚀 Carga finalizada!")

#     print("\n🚀 Carga completa: Finanças, Consumo e Investimentos!")

#     # 2. CARGA DOS DADOS
#     # Agora o schema 'postgres_raw' JÁ EXISTE, então o to_sql vai funcionar
#     try:
#         process_pagamento_dinheiro()
#     except Exception as e:
#         print(f"❌ Erro no Pix: {e}")

#     try:
#         process_pagamento_cartao()
#     except Exception as e:
#         print(f"❌ Erro no Cartão: {e}")

#     print("\n🚀 Carga finalizada!")

import pandas as pd
from sqlalchemy import create_engine, text
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import zipfile
import os
import re
from dotenv import load_dotenv

# 1. CONFIGURAÇÃO DE AMBIENTE
load_dotenv()

# Credenciais Banco
user, password = os.getenv('DB_USER'), os.getenv('DB_PASS')
host, port, db_name = os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME')
db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
engine = create_engine(db_url)

# Credenciais Google Drive
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GOOGLE_DRIVE_INVOICE = os.getenv('GOOGLE_DRIVE_INVOICE')
GOOGLE_DRIVE_CONTROLE = os.getenv('GOOGLE_DRIVE_CONTROLE')

# --- FUNÇÕES DE APOIO ---

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    return build('drive', 'v3', credentials=creds)

def clean_currency(series):
    def clean_single_value(val):
        if pd.isna(val) or val == '' or val == '-': return 0.0
        s = str(val).strip().replace('R$', '')
        if ',' in s:
            if '.' in s: s = s.replace('.', '').replace(',', '.')
            else: s = s.replace(',', '.')
        s = re.sub(r'[^0-9.-]', '', s)
        try: return float(s)
        except ValueError: return 0.0
    return series.apply(clean_single_value)

def get_processed_files():
    """Verifica no banco quais faturas já existem para não duplicar"""
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT DISTINCT arquivo_origem FROM postgres_raw.payment_card", conn)
            return df['arquivo_origem'].tolist()
    except:
        return []

# --- NÚCLEO DE PROCESSAMENTO DRIVE ---

def download_file_to_memory(service, folder_id, file_extension):
    """Busca um arquivo na pasta e traz para a memória"""
    query = f"'{folder_id}' in parents and name contains '{file_extension}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if not files:
        return None, None

    # Pega o primeiro arquivo encontrado (ou o mais recente se precisar de lógica extra)
    file_id = files[0]['id']
    file_name = files[0]['name']
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    
    fh.seek(0)
    return fh, file_name

# --- FUNÇÕES DE CARGA ---

def process_controle_excel(file_buffer):
    """Processa todas as abas da planilha Controle.xlsx"""
    sheets = {
        'payment_pix': 'pagamento',
        'income': 'entrada',
        'nissan_kicks_consumption': 'nissan_kicks_consumption',
        'stock_movements': 'stock_movements'
    }
    
    for table, sheet in sheets.items():
        df = pd.read_excel(file_buffer, sheet_name=sheet)
        df = df.dropna(how='all')
        
        # Limpeza de colunas numéricas
        for col in df.columns:
            if any(k in col.lower() for k in ['valor', 'value', 'preço', 'taxa', 'km', 'litro']):
                df[col] = clean_currency(df[col])
        
        df['arquivo_origem'] = 'Controle.xlsx'
        df.to_sql(table, engine, schema='postgres_raw', if_exists='replace', index=False)
        print(f"✅ Tabela {table} (Aba: {sheet}) atualizada.")

def process_faturas_zip(file_buffer):
    """Abre o ZIP protegido e carrega apenas os CSVs novos"""
    already_done = get_processed_files()
    # Pega a senha do .env e converte para bytes (necessário para o zipfile)
    zip_password = os.getenv('ZIP_PASSWORD')
    pwd_bytes = zip_password.encode('utf-8') if zip_password else None
    
    with zipfile.ZipFile(file_buffer) as z:
        for filename in z.namelist():
            if filename.endswith('.csv'):
                if filename not in already_done:
                    try:
                        # Passamos a senha aqui no pwd=...
                        with z.open(filename, pwd=pwd_bytes) as f:
                            df = pd.read_csv(f, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
                            df = df.dropna(how='all')
                            
                            for col in df.columns:
                                if 'valor' in col.lower():
                                    df[col] = clean_currency(df[col])
                            
                            df['arquivo_origem'] = filename
                            df.to_sql('payment_card', engine, schema='postgres_raw', if_exists='append', index=False)
                            print(f"   ✅ Nova fatura inserida: {filename}")
                    except RuntimeError as e:
                        if "password required" in str(e):
                            print(f"   ❌ Erro: O arquivo {filename} está protegido e a senha no .env está incorreta ou ausente.")
                        else:
                            print(f"   ❌ Erro ao abrir {filename}: {e}")
                else:
                    print(f"   ⏭️ Pulando {filename} (já existe no banco).")

# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    print("🏗️ Iniciando Pipeline de Dados (Google Drive -> Postgres)...")
    service = get_drive_service()

    # 1. Preparar Schema
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS postgres_raw;"))
        conn.commit()

    # 2. Processar Faturas (ZIP)
    print("\n📦 Verificando Faturas no Drive...")
    zip_fh, zip_name = download_file_to_memory(service, GOOGLE_DRIVE_INVOICE, '.zip')
    if zip_fh:
        process_faturas_zip(zip_fh)
    else:
        print("⚠️ Nenhum arquivo ZIP encontrado na pasta de faturas.")

    # 3. Processar Controle (Excel)
    print("\n📊 Verificando Planilha Controle no Drive...")
    xlsx_fh, xlsx_name = download_file_to_memory(service, GOOGLE_DRIVE_CONTROLE, '.xlsx')
    if xlsx_fh:
        process_controle_excel(xlsx_fh)
    else:
        print("⚠️ Planilha Controle.xlsx não encontrada no Drive.")

    print("\n🚀 Pipeline finalizada com sucesso!")