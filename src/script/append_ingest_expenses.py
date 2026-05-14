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
from pathlib import Path

# 1. ENVIRONMENT CONFIGURATION

root_path = Path(__file__).parent.parent.parent
env_path = root_path / '.env'
load_dotenv(dotenv_path=env_path)

# Bank credentials
user, password = os.getenv('DB_USER'), os.getenv('DB_PASS')
host, port, db_name = os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME')
db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
engine = create_engine(db_url)

creds_env_value = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if creds_env_value:
    SERVICE_ACCOUNT_FILE = root_path / creds_env_value
else:
    SERVICE_ACCOUNT_FILE = None

print(f"DEBUG: Caminho Raiz: {root_path}")
print(f"DEBUG: Buscando credenciais em: {SERVICE_ACCOUNT_FILE}")

# USE THIS IF I WANT TO KEEP THE DATA AND JUST APPEND
def prepare_database(engine):
    print("🛠️ Preparing ingestion environment...")
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS postgres_raw;"))
        
        # If you REALLY need to clean the input table (full load model),
        # keep the TRUNCATE only on the specific table, never the DROP SCHEMA.
        # conn.execute(text("TRUNCATE TABLE postgres_raw.payment_card;"))
        
        conn.execute(text("COMMIT;"))
    print("✅ Environment ready to receive raw data.")

# Credentials from Google Drive
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GOOGLE_DRIVE_INVOICE = os.getenv('GOOGLE_DRIVE_INVOICE')
GOOGLE_DRIVE_CONTROLE = os.getenv('GOOGLE_DRIVE_CONTROLE')

creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SERVICE_ACCOUNT_FILE = root_path / creds_path if creds_path else None

print(f"DEBUG: Searching for credentials at: {SERVICE_ACCOUNT_FILE}")

## Backup functions

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
    """Verify in DB which invoices existis to avoid duplicity"""
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT DISTINCT arquivo_origem FROM postgres_raw.payment_card", conn)
            return df['arquivo_origem'].tolist()
    except:
        return []

def download_specific_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# --- LOADING FUNCTION ---

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
        
        # Cleaning numeric columns
        for col in df.columns:
            if any(k in col.lower() for k in ['valor', 'value', 'preço', 'taxa', 'km', 'litro']):
                df[col] = clean_currency(df[col])
        
        df['arquivo_origem'] = 'Controle.xlsx'

        # --- INTEGRATION WITH DBT ---
        with engine.connect() as conn:
            try:
                conn.execute(text(f"TRUNCATE TABLE postgres_raw.{table} CASCADE;"))
                conn.commit()
                current_mode = 'append'
                print(f"🧹 Tabela {table} limpa (Truncate).")
            except Exception:
                conn.rollback()
                current_mode = 'replace'
                print(f"🆕 Tabela {table} será recriada (Replace).")
        
        # Load
        df.to_sql(table, engine, schema='postgres_raw', if_exists=current_mode, index=False)
        print(f"✅ Tabela {table} (Aba: {sheet}) atualizada com sucesso.")

def process_faturas_zip(file_buffer):
    """Open the protected ZIP and load only the new csv"""
    already_done = get_processed_files()
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

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("🏗️ Iniciando Pipeline de Dados (Google Drive -> Postgres)...")
    service = get_drive_service()

    # 1. Prepare schema
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS postgres_raw;"))
        conn.commit()

    # 2. Process invoices
    print("\n📦 Verificando Faturas no Drive...")
    query = f"'{GOOGLE_DRIVE_INVOICE}' in parents and name contains '.zip' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if files:
        print(f"🔍 Encontrados {len(files)} arquivos ZIP. Iniciando processamento...")
        for file in files:
            print(f"👉 Baixando: {file['name']}")
            zip_fh = download_specific_file(service, file['id'])
            process_faturas_zip(zip_fh)
    else:
        print("⚠️ Nenhum arquivo ZIP encontrado na pasta de faturas.")

    # 3. Process Control (Excel)
    print("\n📊 Verificando Planilha Controle no Drive...")
    query_xlsx = f"'{GOOGLE_DRIVE_CONTROLE}' in parents and name contains '.xlsx' and trashed = false"
    results_xlsx = service.files().list(q=query_xlsx, fields="files(id, name)").execute()
    files_xlsx = results_xlsx.get('files', [])

    if files_xlsx:
        file_xlsx = files_xlsx[0]
        print(f"👉 Baixando planilha: {file_xlsx['name']}")
        xlsx_fh = download_specific_file(service, file_xlsx['id'])
        process_controle_excel(xlsx_fh)
    else:
        print("⚠️ Planilha Controle.xlsx não encontrada no Drive.")