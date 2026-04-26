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