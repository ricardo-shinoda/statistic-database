import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import re
import os
import numpy as np
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera as variáveis ou define um padrão (default)
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Monta a URL usando f-string
db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

engine = create_engine(db_url)

# # Ajuste sua senha aqui
# engine = create_engine('postgresql://ricardo:3136@localhost:5432/statistic_db')

def process_pagamento_cartao():
    # Agora olha para a pasta raiz das faturas
    base_path = Path("data_lake/raw_invoices/")
    
    # rglob("*.csv") busca em todas as subpastas recursivamente
    files = list(base_path.rglob("*.csv"))
    
    print(f"📂 Total de faturas encontradas: {len(files)}")
    
    for csv_file in files:
        # Mostra o caminho relativo para você saber qual ano está processando
        print(f"📄 Processando: {csv_file.relative_to(base_path)}")
        
        try:
            # Lendo com separador ';' e ignorando erros de linhas extras
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            df = df.dropna(how='all')

            if df.empty:
                continue

            # MAPEAMENTO REAL (Baseado em 9 colunas):
            # 0: Data | 1: Nome | 2: Cartão | 3: Categoria | 4: DESCRICAO | 5: PARCELA | 8: VALOR BRL
            stg_df = pd.DataFrame({
                'data_compra': pd.to_datetime(df.iloc[:, 0], dayfirst=True, errors='coerce'),
                'cartao_titular': df.iloc[:, 1],
                'cartao_final': df.iloc[:, 2].astype(str),
                'categoria': df.iloc[:, 3],
                'descricao': df.iloc[:, 4], 
                'parcela': df.iloc[:, 5].astype(str).replace('nan', 'Única'), 
                'valor_usd': clean_currency(df.iloc[:, 7]) if df.shape[1] > 7 else 0.0,
                'valor_brl': clean_currency(df.iloc[:, 8]), 
                'arquivo_origem': f"{csv_file.parent.name}/{csv_file.name}" # Salva '2025/arquivo.csv'
            })

            # Remove linhas onde a data ou descrição falharam (cabeçalhos extras, etc)
            stg_df = stg_df.dropna(subset=['data_compra', 'descricao'])
            
            if not stg_df.empty:
                stg_df.to_sql('pagamento_cartao', engine, if_exists='append', index=False)
                print(f"   ✅ {len(stg_df)} registros inseridos.")
                
        except Exception as e:
            print(f"   ❌ Erro ao processar {csv_file.name}: {e}")

def process_pagamento_dinheiro():
    path = "data/raw/Controle.xlsx"
    df = pd.read_excel(path, sheet_name='pagamento')
    
    stg_df = pd.DataFrame({
        'data_compra': pd.to_datetime(df.iloc[:, 0], dayfirst=True, errors='coerce'),
        'descricao': df.iloc[:, 2],
        'valor': clean_currency(df.iloc[:, 3]),
        'status_pagamento': df.iloc[:, 4],
        'parcela': df.iloc[:, 5].astype(str).fillna('1-1'),
        'comentario': df.iloc[:, 6],  # Mudado: agora recebe o que era categoria (coluna 6)
        'categoria': None,  # Vazio por enquanto
        'subcategoria': None,  # Vazio por enquanto
        'metodo_pagamento': df.iloc[:, 8] if df.shape[1] > 8 else None,
        'arquivo_origem': 'Controle.xlsx'
    })
    
    stg_df = stg_df.dropna(subset=['descricao', 'data_compra'])
    stg_df.to_sql('pagamento_dinheiro', engine, if_exists='append', index=False)
    print(f"✅ {len(stg_df)} registros em pagamento_dinheiro.")

def clean_currency(series):
    """Limpa valores monetários, detectando automaticamente formato BR ou US"""
    
    def clean_single_value(val):
        if pd.isna(val) or val == '' or val == '-':
            return 0.0
        
        original = str(val).strip()
        
        # Remove 'R$' if present
        s = original.replace('R$', '').strip()
        
        # Detect format:
        # If it has a comma and the comma is in the last 3 positions (likely decimal)
        # OR if it has both dot and comma (Brazilian format)
        if ',' in s:
            if '.' in s:
                # Brazilian format: 2.524,52
                # Remove dots, replace comma with dot
                s = s.replace('.', '').replace(',', '.')
            else:
                # Only comma: like "365,39" - Brazilian format without thousand separator
                s = s.replace(',', '.')
        else:
            # US format or already numeric: like "32.0" or "2524.52"
            # Remove any non-numeric except dot
            import re
            s = re.sub(r'[^0-9.-]', '', s)
        
        # Remove any remaining non-numeric characters except dot and minus
        import re
        s = re.sub(r'[^0-9.-]', '', s)
        
        try:
            return float(s)
        except ValueError:
            return 0.0
    
    return series.apply(clean_single_value)

if __name__ == "__main__":
    with engine.begin() as conn:
        print("🧹 Limpando tabelas staging...")
        conn.execute(text("TRUNCATE TABLE pagamento_dinheiro, pagamento_cartao RESTART IDENTITY;"))
    
    # Processa Dinheiro
    try:
        process_pagamento_dinheiro()
    except Exception as e:
        print(f"❌ Erro crítico no processamento de Dinheiro: {e}")

    # Processa Cartão (mesmo que o dinheiro falhe)
    try:
        process_pagamento_cartao()
    except Exception as e:
        print(f"❌ Erro crítico no processamento de Cartão: {e}")

    print("\n🚀 Fim do script.")
    print("\n🚀 Tudo pronto!")