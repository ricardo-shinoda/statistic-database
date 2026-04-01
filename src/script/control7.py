# Complete table with expenses from CC and pix, investments, now adding car comsumption
import os
import zipfile
import shutil
import pandas as pd
import pathlib
from sqlalchemy import create_engine, text
from decouple import config
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# --- CONFIGURAÇÃO ---
CURRENT_MONTH = "2023-04" 
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'
ZIP_PASSWORD = config('ZIP_PASSWORD')

# Navegação de diretórios
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
LAKE_DIR = ROOT_DIR / "data_lake" / "raw_invoices"

# Arquivos
CONTROLE_XLSX = DATA_DIR / "raw" / "Controle.xlsx"
ZIP_PATH = pathlib.Path("/home/ricardo/Downloads/Fatura-CPF.zip")

engine = create_engine(DB_URL)

# --- FUNÇÕES AUXILIARES ---

def clean_currency(series):
    """Limpa strings de moeda mantendo a lógica decimal correta."""
    if series.dtype != 'object':
        return series
    # Remove R$, espaços e pontos de milhar, depois troca vírgula por ponto
    clean = series.astype(str).str.replace(r'[R\$\s]', '', regex=True)
    # Se o número for algo como 1.234,56 -> removemos o ponto do milhar
    clean = clean.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    return clean

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
        if os.path.exists(ZIP_PATH): os.remove(ZIP_PATH) 
        return final_path
    return final_path if os.path.exists(final_path) else None

def process_credit_card(path):
    if not path or not os.path.exists(path): return pd.DataFrame()
    
    # 1. Lê com o separador correto (;)
    df = pd.read_csv(path, sep=';', encoding='utf-8') 
    
    # --- CARREGAR O JSON DE MAPPING ---
    # Caminho exato: statistic/data/mapping/description.json
    json_path = DATA_DIR / "mapping" / "description.json"
    lookup = {}
    if os.path.exists(json_path):
        import json
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cat_map = json.load(f)
            # Dicionário: { 'NOME NO CSV': ('CATEGORIA', 'SUBCATEGORIA') }
            lookup = {item['original']: (item['categoria'], item['subcategoria']) for item in cat_map}
        except Exception as e:
            print(f"⚠️ Erro ao ler JSON: {e}")
    # ----------------------------------

    # 2. Mapeamento inicial das colunas do CSV
    mapping = {
        'Data de Compra': 'transaction_date',
        'Descrição': 'description',
        'Valor (em R$)': 'amount_brl',
        'Categoria': 'raw_category', # Chamamos de raw para decidir depois
        'Nome no Cartão': 'card_holder_name'
    }
    df = df.rename(columns=mapping)

    # 3. LÓGICA DE CATEGORIZAÇÃO HÍBRIDA
    def enrich_categories(row):
        desc = row['description']
        # Se achou no JSON, usa o do JSON
        if desc in lookup:
            return lookup[desc][0], lookup[desc][1]
        # Se NÃO achou, mantém a 'raw_category' do CSV e marca subcategoria como pendente
        return row['raw_category'], "Aguardando Classificação"

    # Aplica a função linha a linha
    df[['category', 'subcategory']] = df.apply(
        lambda x: pd.Series(enrich_categories(x)), axis=1
    )

    # 4. Limpeza dos dados numéricos e data
    if 'amount_brl' in df.columns:
        df['amount_brl'] = pd.to_numeric(clean_currency(df['amount_brl']), errors='coerce').fillna(0)
    
    if 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, errors='coerce')

    # Metadados
    df['source_file'] = os.path.basename(path)
    df['transaction_type'] = 'credit_card'
    
    # 5. Seleção Final (Garante que a 'raw_category' não vá para o banco, apenas a 'category' tratada)
    valid_cols = [
        'transaction_date', 'description', 'category', 'subcategory', 
        'amount_brl', 'card_holder_name', 'source_file', 'transaction_type'
    ]
    
    return df[[c for c in valid_cols if c in df.columns]]

def process_manual_bills():
    if not os.path.exists(CONTROLE_XLSX): return pd.DataFrame()
    xl = pd.ExcelFile(CONTROLE_XLSX)
    sheet = next((s for s in xl.sheet_names if s.lower() == 'contas a pagar'), None)
    if not sheet: return pd.DataFrame()
    
    df = pd.read_excel(xl, sheet_name=sheet).dropna(how='all')
    df = df.dropna(subset=['Descrição'])
    df['amount_brl'] = pd.to_numeric(clean_currency(df['Quanto']), errors='coerce').fillna(0)
    
    return pd.DataFrame({
        'transaction_date': pd.to_datetime(df['Dia']),
        'description': df['Descrição'].str.strip(),
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
            'organization': ['organization', 'instituição financeira'],
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

def process_vehicle_consumption():
    if not os.path.exists(CONTROLE_XLSX): return pd.DataFrame()
    try:
        # Agora podemos ler deixando o Pandas identificar os tipos, 
        # já que os dados estão limpos!
        df = pd.read_excel(CONTROLE_XLSX, sheet_name='Consumo Nissan Kicks')
        
        # Limpa espaços nos nomes das colunas
        df.columns = [str(c).strip() for c in df.columns]

        # Converte a data garantindo o formato correto
        df['filling_date'] = pd.to_datetime(df['filling_date'], errors='coerce')
        
        # O que for numérico, garantimos que seja float e preenchemos vazios com 0
        numeric_cols = [
            'odometer_reading', 'total_amount_paid', 'discount_amount', 
            'volume_liters', 'price_per_liter', 'kmv_points', 'cashback_amount',
            'comp_price_per_liter', 'board_consumption_kml', 'board_avg_speed_kmh',
            'board_trip_distance_km', 'board_remaining_range_km'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Remove linhas sem data
        df = df.dropna(subset=['filling_date'])

        return df

    except Exception as e:
        print(f"⚠️ Erro no processamento dos dados limpos: {e}")
        return pd.DataFrame()
        
# --- PIPELINE ---

def run_pipeline(month):
    print(f"🚀 Iniciando Pipeline de Engenharia (Full Refresh)...")

    # 1. Cartão
    csv_path = ingest_and_archive(month)
    if csv_path:
        df_cc = process_credit_card(csv_path)
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM fact_transactions WHERE source_file = :f"), {"f": f"invoice-{month}.csv"})
        df_cc.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"💳 Cartão ({month}): {len(df_cc)} linhas.")

    # 2. Contas
    df_m = process_manual_bills()
    if not df_m.empty:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM fact_transactions WHERE transaction_type = 'manual_bill'"))
        df_m.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"📝 Contas a Pagar: {len(df_m)} linhas.")

    # 3. Investimentos
    df_i = process_investments()
    if not df_i.empty:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE fact_investments RESTART IDENTITY"))
        df_i.to_sql('fact_investments', engine, if_exists='append', index=False)
        print(f"📈 Investimentos: {len(df_i)} linhas.")

    # 4. Nissan
    df_v = process_vehicle_consumption()
    if not df_v.empty:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE fact_vehicle_fueling RESTART IDENTITY"))
        df_v.to_sql('fact_vehicle_fueling', engine, if_exists='append', index=False)
        print(f"🚗 Nissan Kicks: {len(df_v)} registros processados.")
    
    print("✨ Sync completo!")

if __name__ == "__main__":
    run_pipeline(CURRENT_MONTH)