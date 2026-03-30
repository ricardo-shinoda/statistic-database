import os
import zipfile
import shutil
import pandas as pd
from sqlalchemy import create_engine, text
from decouple import config

import pathlib
from sqlalchemy import create_engine, text
from decouple import config

# --- CONFIGURAÇÃO ---
CURRENT_MONTH = "2021-06" 
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'
ZIP_PASSWORD = config('ZIP_PASSWORD')

# Localização do script atual: STATISTIC/src/script/control6.py
# .parent (script/) -> .parent (src/) -> .parent (STATISTIC/ raiz)
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

# Novos caminhos organizados
DATA_DIR = ROOT_DIR / "data"
LAKE_DIR = ROOT_DIR / "data_lake" / "raw_invoices"

# Arquivos específicos
CONTROLE_XLSX = DATA_DIR / "Controle.xlsx"
ZIP_PATH = pathlib.Path("/home/ricardo/Downloads/Fatura-CPF.zip")

engine = create_engine(DB_URL)

# --- FUNÇÕES AUXILIARES ---

def classify_asset(ticker):
    ticker_str = str(ticker).upper()
    rf_terms = ['CDB', 'TESOURO', 'LCI', 'LCA', 'SELIC']
    return 'Renda Fixa' if any(t in ticker_str for t in rf_terms) else 'Renda Variável'

def ingest_and_archive(invoice_month):
    year = invoice_month.split('-')[0]
    target_folder = os.path.join(LAKE_DIR, year)
    os.makedirs(target_folder, exist_ok=True)
    
    final_path = os.path.join(target_folder, f"invoice-{invoice_month}.csv")
    
    if os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, 'r') as z:
            csv_name = z.namelist()[0]
            z.extract(csv_name, "/tmp", pwd=bytes(ZIP_PASSWORD, 'utf-8'))
        
        shutil.move(f"/tmp/{csv_name}", final_path)
        os.remove(ZIP_PATH) # Limpeza automática do Downloads
        return final_path
    
    return final_path if os.path.exists(final_path) else None

def process_credit_card(path):
    df = pd.read_csv(path)
    # Aqui vai sua lógica de limpeza do CSV do cartão (colunas, datas, etc)
    # Exemplo simplificado para o pipeline rodar:
    df['source_file'] = os.path.basename(path)
    df['transaction_type'] = 'credit_card'
    return df

def process_manual_bills():
    if not os.path.exists(CONTROLE_XLSX): return pd.DataFrame()
    xl = pd.ExcelFile(CONTROLE_XLSX)
    sheet = next((s for s in xl.sheet_names if s.lower() == 'contas a pagar'), None)
    if not sheet: return pd.DataFrame()
    
    # Lê a aba e remove linhas totalmente vazias
    df = pd.read_excel(xl, sheet_name=sheet).dropna(how='all')
    
    # --- LIMPEZA DE DADOS (DATA CLEANING) ---
    # 1. Garante que a descrição não seja nula e remove espaços extras
    df = df.dropna(subset=['Descrição'])
    
    # 2. Limpeza de valores
    df['amount_brl'] = df['Quanto'].astype(str).replace(r'[R\$\s.]', '', regex=True).replace(',', '.', regex=True)
    df['amount_brl'] = pd.to_numeric(df['amount_brl'], errors='coerce').fillna(0)
    
    # 3. Filtra apenas o que tem valor maior que zero (remove linhas vazias de valor)
    df = df[df['amount_brl'] > 0]
    
    return pd.DataFrame({
        'transaction_date': pd.to_datetime(df['Dia']),
        'description': df['Descrição'].str.strip(), # Remove espaços inúteis
        'amount_brl': df['amount_brl'],
        'transaction_type': 'manual_bill',
        'source_file': 'Controle.xlsx'
    })

def process_investments():
    if not os.path.exists(CONTROLE_XLSX): return pd.DataFrame()
    try:
        xl = pd.ExcelFile(CONTROLE_XLSX)
        target_sheet = 'Movements' 
        
        if target_sheet not in xl.sheet_names:
            print(f"⚠️ Aba {target_sheet} não encontrada!")
            return pd.DataFrame()

        df = pd.read_excel(xl, sheet_name=target_sheet)
        
        # Normaliza nomes das colunas: minúsculo e sem espaços
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Mapeamento flexível de nomes (ajustado para evitar o erro de float64)
        col_map = {
            'owner': ['investor', 'owner', 'proprietário'],
            'transaction_type': ['transaction_type', 'order', 'tipo'],
            'transaction_date': ['transaction_date', 'data', 'date'],
            'ticker': ['ticker', 'ativo'],
            'quantity': ['quantity', 'qtt', 'quantidade'],
            'unit_price': ['unit$', 'unit price', 'preço unitário'],
            'total_amount': ['total_amount', 'total'],
            'cnpj': ['cnpj']
        }

        # Função para pegar a coluna correta do DF original
        def get_actual_col(options):
            for opt in options:
                if opt in df.columns: return df[opt]
            return pd.Series([None] * len(df)) # Retorna coluna vazia se não achar

        # Construção do DataFrame com tratamento de erros direto
        # --- ETAPA 2: Construção do DataFrame com Boas Práticas de Engenharia ---
        processed_df = pd.DataFrame()
        
        # 1. Normalização de Texto (Lowercase para busca e agrupamento)
        processed_df['owner'] = get_actual_col(col_map['owner']).astype(str).str.lower().str.strip()
        processed_df['transaction_type'] = get_actual_col(col_map['transaction_type']).astype(str).str.lower().str.strip()
        
        # 2. Normalização de Tickers (UPPERCASE - Padrão de mercado B3/APIs)
        processed_df['ticker'] = get_actual_col(col_map['ticker']).astype(str).str.upper().str.strip()
        
        # 3. Datas e Metadados
        processed_df['transaction_date'] = pd.to_datetime(get_actual_col(col_map['transaction_date']), dayfirst=True, errors='coerce')
        processed_df['asset_type'] = processed_df['ticker'].apply(classify_asset)
        
        # 4. Tratamento Numérico (Quantity)
        processed_df['quantity'] = pd.to_numeric(get_actual_col(col_map['quantity']), errors='coerce').fillna(0)
        
        # 5. Limpeza de Moeda (R$) para unit_price e total_amount
        for col in ['unit_price', 'total_amount']:
            raw_val = get_actual_col(col_map[col]).astype(str)
            clean_val = raw_val.str.replace(r'[R\$\s.]', '', regex=True).str.replace(',', '.', regex=True)
            processed_df[col] = pd.to_numeric(clean_val, errors='coerce').fillna(0)

        # NOTA: Removemos a linha do CNPJ daqui! 
        # Ele agora será consultado via JOIN com a dim_assets no seu SQL.

        # Remove linhas sem data (limpeza de lixo do Excel)
        return processed_df.dropna(subset=['transaction_date'])

    except Exception as e:
        print(f"⚠️ Erro ao processar Investimentos: {e}")
        return pd.DataFrame()

# --- PIPELINE PRINCIPAL ---

def run_pipeline(month):
    print(f"🚀 Iniciando Pipeline 2.0...")

    # 1. Cartão de Crédito
    csv_path = ingest_and_archive(month)
    if csv_path:
        df_cc = process_credit_card(csv_path)
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM fact_transactions WHERE source_file = :f"), {"f": f"invoice-{month}.csv"})
        df_cc.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"💳 Cartão ({month}): {len(df_cc)} linhas.")

    # 2. Contas a Pagar (Manual)
    df_m = process_manual_bills()
    if not df_m.empty:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM fact_transactions WHERE transaction_type = 'manual_bill'"))
        df_m.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"📝 Contas a Pagar: {len(df_m)} linhas.")

    # 3. Investimentos (Stock-Statistic)
    df_i = process_investments()
    if not df_i.empty:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM fact_investments"))
        df_i.to_sql('fact_investments', engine, if_exists='append', index=False)
        print(f"📈 Investimentos: {len(df_i)} linhas.")
    
    print("✨ Sync completo!")

if __name__ == "__main__":
    run_pipeline(CURRENT_MONTH)