import os
import zipfile
import shutil
import pandas as pd
import pathlib
import json
from sqlalchemy import create_engine, text
from decouple import config
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
load_dotenv()

# Mês atual para o processamento padrão via ZIP
CURRENT_MONTH = "2026-04" 
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'
ZIP_PASSWORD = config('ZIP_PASSWORD')

# Navegação de diretórios
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
LAKE_DIR = ROOT_DIR / "data_lake" / "raw_invoices"
HISTORICAL_XLSX_DIR = ROOT_DIR / "src" / "credit_card" / "xlsx"

# Arquivos
CONTROLE_XLSX = DATA_DIR / "raw" / "Controle.xlsx"
ZIP_PATH = pathlib.Path("/home/ricardo/Downloads/Fatura-CPF.zip")

engine = create_engine(DB_URL)

# --- FUNÇÕES AUXILIARES ---

def clean_currency(series):
    if series.dtype != 'object':
        return series
    clean = series.astype(str).str.replace(r'[R\$\s]', '', regex=True)
    clean = clean.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    return clean

def load_mapping_lookup():
    json_path = DATA_DIR / "mapping" / "description.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cat_map = json.load(f)
            return {item['original'].strip().upper(): (item['categoria'], item['subcategoria']) for item in cat_map}
        except Exception as e:
            print(f"⚠️ Erro ao ler JSON de mapping: {e}")
    return {}

# --- CORE DE PROCESSAMENTO (CREDIT CARD) ---

def process_credit_card(path):
    if not path or not os.path.exists(path): 
        print(f"❌ Arquivo não encontrado: {path}")
        return pd.DataFrame()
    
    file_name = os.path.basename(path)
    ext = pathlib.Path(path).suffix.lower()

    try:
        if ext == '.csv':
            try:
                df = pd.read_csv(path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(path, sep=';', encoding='latin1')
        else:
            df = pd.read_excel(path)
    except Exception as e:
        print(f"⚠️ Erro crítico na leitura de {file_name}: {e}")
        return pd.DataFrame()

    if df.empty: return pd.DataFrame()

    # Normalização de Colunas (ASCII para evitar caracteres estranhos)
    df.columns = [c.encode('ascii', 'ignore').decode('ascii').strip() if isinstance(c, str) else c for c in df.columns]

    mapping = {
        'Data de Compra': 'transaction_date',
        'Data': 'transaction_date',
        'Descricao': 'description',
        'Descrio': 'description',
        'Valor (em R$)': 'amount_brl',
        'Valor': 'amount_brl',
        'Categoria': 'raw_category'
    }
    df = df.rename(columns=mapping)

    # Limpeza de Valores e Datas
    df['amount_brl'] = pd.to_numeric(clean_currency(df['amount_brl']), errors='coerce').fillna(0)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce', dayfirst=True)
    
    if df['transaction_date'].isna().any():
        try:
            parts = file_name.replace('invoice-', '').split('-')
            fallback = pd.to_datetime(f"{parts[0]}-{parts[1]}-01")
            df['transaction_date'] = df['transaction_date'].fillna(fallback)
        except: pass

    df['source_file'] = file_name
    return df

# --- NOVAS FUNÇÕES DE INGESTÃO (STAGING) ---

def ingest_to_staging(df, table_name):
    """Auxiliar para limpar e inserir dados na Staging sem frescuras."""
    if df.empty: return
    
    df['ingestion_at'] = pd.to_datetime('now')
    
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name}"))
        df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"📥 Staging '{table_name}' atualizada: {len(df)} linhas.")

def process_outflow_excel():
    """Lê a aba 'outflow' da sua planilha Controle.xlsx"""
    if not os.path.exists(CONTROLE_XLSX): return
        
    try:
        # Lemos a aba 'outflow'
        df = pd.read_excel(CONTROLE_XLSX, sheet_name='outflow')
        
        mapping = {
            'transaction_date': 'transaction_date',
            'description': 'description',
            'amount': 'amount',
            'status': 'status',
            'installment': 'installment',
            'payment_method': 'payment_method',
            'payee_document': 'payee_document',
            'income_tax_applicable': 'income_tax_applicable'
        }
        
        df = df[[c for c in mapping.keys() if c in df.columns]]
        df['amount'] = pd.to_numeric(clean_currency(df['amount']), errors='coerce')
        
        ingest_to_staging(df, 'stg_outflow')
        
    except Exception as e:
        print(f"⚠️ Erro ao processar aba Outflow: {e}")

def process_inflow_excel():
    """Lê a aba 'inflow' da sua planilha Controle.xlsx"""
    if not os.path.exists(CONTROLE_XLSX): return
    try:
        df = pd.read_excel(CONTROLE_XLSX, sheet_name='inflow')
        # Mapeamento similar ao outflow
        df['amount'] = pd.to_numeric(clean_currency(df['amount']), errors='coerce')
        ingest_to_staging(df, 'stg_inflow')
    except Exception as e:
        print(f"⚠️ Erro ao processar aba Inflow: {e}")

def process_credit_card_to_staging(path):
    """Lê o CSV da fatura e joga na Staging Raw do Cartão"""
    df = process_credit_card(path)
    
    if not df.empty:
        # Mapeia para stg_credit_card
        stg_df = pd.DataFrame({
            'purchase_date': df['transaction_date'].dt.strftime('%Y-%m-%d'),
            'raw_category_description': df['description'],
            'installment': df.get('installment', '1/1'),
            'amount_brl': df['amount_brl'],
            'source_file': df['source_file']
        })
        ingest_to_staging(stg_df, 'stg_credit_card')

# --- CAMADA DE TRANSFORMAÇÃO (SILVER) ---

def transform_staging_to_fact():
    """Executa a lógica SQL para consolidar as Stagings na Fact."""
    sql = """
    -- Limpa registros para evitar duplicidade na Fact
    DELETE FROM fact_transactions WHERE source_type IN ('excel_outflow', 'csv_credit');

    -- Insere Outflow (Pix/Cash)
    INSERT INTO fact_transactions (transaction_date, description, amount, payment_status, payment_method, is_tax_deductible, source_type)
    SELECT 
        transaction_date::DATE, description, amount, status, payment_method, 
        CASE WHEN income_tax_applicable = 'Yes' THEN TRUE ELSE FALSE END,
        'excel_outflow'
    FROM stg_outflow;

    -- Insere Credit Card
    INSERT INTO fact_transactions (transaction_date, description, amount, payment_status, payment_method, source_type)
    SELECT 
        purchase_date::DATE, raw_category_description, amount_brl, 'paid', 'credit_card', 'csv_credit'
    FROM stg_credit_card;
    """
    with engine.begin() as conn:
        conn.execute(text(sql))
    print("🚀 Fact Transactions atualizada via SQL.")

# --- RUNNER ---

def run_pipeline(mode="current", target_file=None):
    print(f"🚀 Iniciando Pipeline em modo: {mode}")

    # 1. Ingestão do Cartão (CSV -> STG)
    # Lógica simplificada: se houver arquivo no Lake para o mês atual
    year = CURRENT_MONTH.split('-')[0]
    final_path = LAKE_DIR / year / f"invoice-{CURRENT_MONTH}.csv"
    
    if final_path.exists():
        process_credit_card_to_staging(str(final_path))

    # 2. Ingestão do Excel (Outflow & Inflow -> STG)
    process_outflow_excel()
    process_inflow_excel()

    # 3. Transformação (STG -> FACT)
    transform_staging_to_fact()

    print("✨ Dados processados e unificados com sucesso!")

if __name__ == "__main__":
    run_pipeline(mode="current")