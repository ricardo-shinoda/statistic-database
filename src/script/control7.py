import os
import zipfile
import shutil
import pandas as pd
import pathlib
import json
from sqlalchemy import create_engine, text
from decouple import config
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# --- CONFIGURAÇÃO ---
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

def classify_asset(ticker):
    ticker_str = str(ticker).upper()
    rf_terms = ['CDB', 'TESOURO', 'LCI', 'LCA', 'SELIC']
    return 'Renda Fixa' if any(t in ticker_str for t in rf_terms) else 'Renda Variável'

def load_mapping_lookup():
    json_path = DATA_DIR / "mapping" / "description.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cat_map = json.load(f)
            return {item['original']: (item['categoria'], item['subcategoria']) for item in cat_map}
        except Exception as e:
            print(f"⚠️ Erro ao ler JSON de mapping: {e}")
    return {}

# --- CORE DE PROCESSAMENTO ---

def process_credit_card(path):
    if not path or not os.path.exists(path): 
        print(f"❌ Arquivo não encontrado: {path}")
        return pd.DataFrame()
    
    file_name = os.path.basename(path)
    # --- CORREÇÃO DO ERRO 'ext' ---
    ext = pathlib.Path(path).suffix.lower()

    # 1. Leitura com Robusteza de Encoding (Resgatando 2019)
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

    if df.empty:
        return pd.DataFrame()

    # 2. Normalização de Colunas (Remove o lixo de encoding 'Ã§Ã£')
    df.columns = [
        c.encode('ascii', 'ignore').decode('ascii').strip() 
        if isinstance(c, str) else c for c in df.columns
    ]

    # 3. Mapeamento Flexível
    mapping = {
        'Data de Compra': 'transaction_date',
        'Data': 'transaction_date',
        'Descricao': 'description', # Nome limpo pós-ascii
        'Descrio': 'description',
        'Valor (em R$)': 'amount_brl',
        'Valor': 'amount_brl',
        'Categoria': 'raw_category',
        'Nome no Cartao': 'card_holder_name'
    }
    df = df.rename(columns=mapping)

    # 4. Enriquecimento de Categorias (Lógica que você quer melhorar)
    lookup = load_mapping_lookup()

    def enrich(row):
        desc_raw = row.get('description', '')
        # Limpamos espaços e deixamos em maiúsculo para o match ser exato
        desc = str(desc_raw).strip().upper() if pd.notna(desc_raw) else ""
        
        if not desc or desc in ['NAN', 'NONE', '']:
            return "Outros", "Aguardando Classificacao"

        # Tenta o Match exato no seu description.json
        if desc in lookup:
            return lookup[desc][0], lookup[desc][1]
        
        # Se não achar no JSON, tenta usar a categoria que veio do Banco/Excel
        cat_orig = row.get('raw_category', 'Outros')
        cat_orig = str(cat_orig).strip() if pd.notna(cat_orig) else "Outros"
        
        return cat_orig, "Revisar Subcategoria"

    # Aplicando a classificação
    results = df.apply(enrich, axis=1)
    df['category'] = [res[0] for res in results]
    df['subcategory'] = [res[1] for res in results]

    # 5. Limpeza de Valores e Datas
    df['amount_brl'] = pd.to_numeric(clean_currency(df['amount_brl']), errors='coerce').fillna(0)
    
    # Tratamento de data (Mixed para lidar com 2019 e 2026 no mesmo pipeline)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce', dayfirst=True)
    
    # Se a data falhou (ex: parcelas 9/10), usamos a data do arquivo
    if df['transaction_date'].isna().any():
        try:
            parts = file_name.replace('invoice-', '').split('-')
            fallback = pd.to_datetime(f"{parts[0]}-{parts[1]}-01")
            df['transaction_date'] = df['transaction_date'].fillna(fallback)
        except:
            pass

    df['source_file'] = file_name
    df['transaction_type'] = 'credit_card'
    
    target_columns = [
        'transaction_date', 'description', 'category', 'subcategory', 
        'amount_brl', 'card_holder_name', 'source_file', 'transaction_type'
    ]
    
    return df[[c for c in target_columns if c in df.columns]]

    # 5. Aplicação Segura (Evita o erro de length de colunas)
    enriched_results = df.apply(enrich, axis=1)
    df['category'] = [res[0] for res in enriched_results]
    df['subcategory'] = [res[1] for res in enriched_results]

    # 6. Limpeza de Tipos e Metadados
    df['amount_brl'] = pd.to_numeric(clean_currency(df['amount_brl']), errors='coerce').fillna(0)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, errors='coerce')
    df['source_file'] = file_name
    df['transaction_type'] = 'credit_card'
    
    # 7. Seleção Final de Colunas (Filtra apenas o que vai para o Postgres)
    target_columns = [
        'transaction_date', 'description', 'category', 'subcategory', 
        'amount_brl', 'card_holder_name', 'source_file', 'transaction_type'
    ]
    
    # Garante que só retornamos colunas que existem no DF para evitar erro de KeyError
    final_cols = [c for c in target_columns if c in df.columns]
    
    return df[final_cols]

def ingest_historical_file(file_name):
    """Lê o arquivo da pasta xlsx, salva uma CÓPIA INTEGRAL no lake e depois ingere no banco."""
    file_path = HISTORICAL_XLSX_DIR / file_name
    
    if not file_path.exists():
        print(f"❌ Arquivo histórico não encontrado em: {file_path}")
        return

    print(f"⏳ Iniciando processamento histórico: {file_name}...")

    # --- 1. GARANTIR A CÓPIA INTEGRAL NO DATA LAKE ---
    # Lemos o Excel bruto sem filtros
    try:
        df_raw = pd.read_excel(file_path)
        
        # Define o destino no Lake
        year = file_name.split('-')[0]
        target_folder = LAKE_DIR / year
        target_folder.mkdir(parents=True, exist_ok=True)
        
        csv_name = f"invoice-{file_name.replace('.xlsx', '.csv').replace('.csv', '')}.csv"
        final_csv_path = target_folder / csv_name
        
        # Salva TUDO o que estava no Excel (inclusive parcelas 9/10, etc) no Data Lake
        df_raw.to_csv(final_csv_path, index=False, sep=';', encoding='utf-8')
        print(f"📂 Cópia INTEGRAL salva no Lake: {final_csv_path}")
        
    except Exception as e:
        print(f"⚠️ Erro ao gerar cópia para o Lake: {e}")
        return

    # --- 2. PROCESSAMENTO PARA O BANCO DE DADOS ---
    # Agora usamos a função que limpa e filtra para o Postgres
    df_cc = process_credit_card(str(final_csv_path)) # Lemos a partir do CSV gerado
    
    if not df_cc.empty:
        with engine.begin() as conn:
            # Remove duplicados baseados no nome do arquivo original
            conn.execute(text("DELETE FROM fact_transactions WHERE source_file = :f"), {"f": file_name})
        
        df_cc.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"✅ Banco atualizado! {len(df_cc)} linhas inseridas.")
# --- RESTO DO PIPELINE (MANUAL/INVESTIMENTOS/VEICULO) ---

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
    # ... (Sua lógica de investimentos permanece idêntica aqui para manter o arquivo funcional)
    # [Mantido conforme seu código anterior para garantir a integridade do pipeline]
    return pd.DataFrame() # Simplificado para o exemplo, use sua versão completa.

def process_vehicle_consumption():
    # ... (Sua lógica do Nissan Kicks permanece idêntica)
    return pd.DataFrame() # Simplificado para o exemplo, use sua versão completa.

# --- RUNNER ---

def run_pipeline(mode="current", target_file=None):
    print(f"🚀 Modo: {mode.upper()}")

    if mode == "historical" and target_file:
        ingest_historical_file(target_file)
    else:
        # Lógica padrão para o ZIP do mês atual
        year = CURRENT_MONTH.split('-')[0]
        target_folder = LAKE_DIR / year
        target_folder.mkdir(parents=True, exist_ok=True)
        final_path = target_folder / f"invoice-{CURRENT_MONTH}.csv"
        
        if ZIP_PATH.exists():
            with zipfile.ZipFile(ZIP_PATH, 'r') as z:
                csv_name = z.namelist()[0]
                z.extract(csv_name, "/tmp", pwd=bytes(ZIP_PASSWORD, 'utf-8'))
            shutil.move(f"/tmp/{csv_name}", final_path)
            os.remove(ZIP_PATH)
        
        if final_path.exists():
            df_cc = process_credit_card(str(final_path))
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM fact_transactions WHERE source_file = :f"), {"f": final_path.name})
            df_cc.to_sql('fact_transactions', engine, if_exists='append', index=False)
            print(f"💳 Atual ({CURRENT_MONTH}): {len(df_cc)} linhas.")

    # Sincroniza as outras tabelas (Contas, Investimentos, Veículo)
    # Estas rodam sempre como Full Refresh do Controle.xlsx
    df_m = process_manual_bills()
    if not df_m.empty:
        with engine.begin() as conn: conn.execute(text("DELETE FROM fact_transactions WHERE transaction_type = 'manual_bill'"))
        df_m.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print("📝 Contas Sync.")

    print("✨ Processo Finalizado!")

if __name__ == "__main__":
    # --- COMO USAR ---
    # Para o mês atual: run_pipeline(mode="current")
    # Para um histórico específico: run_pipeline(mode="historical", target_file="2023-01.xlsx")
    
    run_pipeline(mode="current") 
    # run_pipeline(mode="historical", target_file=f"{CURRENT_MONTH}.xlsx")