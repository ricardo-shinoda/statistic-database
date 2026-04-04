import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import re
import numpy as np

# Ajuste sua senha aqui
engine = create_engine('postgresql://ricardo:3136@localhost:5432/statistic_db')

def clean_currency(column):
    if column is None: return 0.0
    return pd.to_numeric(
        column.replace(r'[\. ]', '', regex=True).replace(',', '.', regex=True), 
        errors='coerce'
    ).fillna(0.0)

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
        'valor': clean_currency(df.iloc[:, 3]), # Limpeza corrigida aqui também
        'status_pagamento': df.iloc[:, 4],
        'parcela': df.iloc[:, 5].astype(str).fillna('1-1'),
        'categoria': df.iloc[:, 6],
        'metodo_pagamento': df.iloc[:, 8] if df.shape[1] > 8 else None,
        'comentario': df.iloc[:, 7] if df.shape[1] > 7 else None,
        'arquivo_origem': 'Controle.xlsx'
    })
    
    stg_df = stg_df.dropna(subset=['descricao', 'data_compra'])
    stg_df.to_sql('pagamento_dinheiro', engine, if_exists='append', index=False)
    print(f"✅ {len(stg_df)} registros em pagamento_dinheiro.")

def clean_currency(series):
    """Limpa R$, pontos de milhar e hífens, garantindo o decimal correto"""
    s = series.astype(str).str.replace('R$', '', regex=False).str.strip()
    s = s.replace(r'^-$', '0', regex=True)
    
    # A mágica aqui: removemos o ponto que separa milhar e trocamos a vírgula pelo ponto decimal
    s = s.str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    
    # Se ainda houver algo que não é número ou ponto, removemos
    s = s.str.replace(r'[^0-9.]', '', regex=True)
    
    return pd.to_numeric(s, errors='coerce').fillna(0.0)

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