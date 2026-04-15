import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os
import re
from dotenv import load_dotenv

# 1. CONFIGURAÇÃO DE AMBIENTE
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
engine = create_engine(db_url)

# 2. FUNÇÃO DE LIMPEZA MÍNIMA (Essencial para o Python não quebrar o Float)
def clean_currency(series):
    def clean_single_value(val):
        if pd.isna(val) or val == '' or val == '-':
            return 0.0
        s = str(val).strip().replace('R$', '')
        if ',' in s:
            if '.' in s: s = s.replace('.', '').replace(',', '.')
            else: s = s.replace(',', '.')
        s = re.sub(r'[^0-9.-]', '', s)
        try:
            return float(s)
        except ValueError:
            return 0.0
    return series.apply(clean_single_value)

# 3. PROCESSAMENTO DE CARTÃO (Extract & Load)
def process_pagamento_cartao():
    base_path = Path("/home/ricardo/study/statistic/data_lake/raw_invoices/")
    files = list(base_path.rglob("*.csv"))
    
    print(f"📂 Faturas encontradas: {len(files)}")
    
    for csv_file in files:
        try:
            # Lê o CSV bruto
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            df = df.dropna(how='all')

            if not df.empty:
                # Adiciona apenas metadado de origem
                df['arquivo_origem'] = f"{csv_file.parent.name}/{csv_file.name}"
                
                # Garante que as colunas de valor sejam numéricas antes de subir
                # No dbt você usará o nome original da coluna (ex: "Valor (em R$)")
                for col in df.columns:
                    if 'valor' in col.lower():
                        df[col] = clean_currency(df[col])

                # Sobe para o schema postgres_raw
                df.to_sql('payment_card', engine, schema='postgres_raw', if_exists='append', index=False)
                print(f"   ✅ {csv_file.name} inserido.")
        except Exception as e:
            print(f"   ❌ Erro em {csv_file.name}: {e}")

# 4. PROCESSAMENTO DE PIX/DINHEIRO (Extract & Load)
def process_pagamento_dinheiro():
    path = "/home/ricardo/study/statistic/data/raw/Controle.xlsx"
    if not os.path.exists(path):
        print(f"⚠️ Arquivo {path} não encontrado.")
        return

    # Lê a aba inteira. Se o dbt precisar de colunas novas, basta mudar o SQL lá.
    df = pd.read_excel(path, sheet_name='pagamento')
    df = df.dropna(how='all')
    
    # Limpeza básica de valor
    for col in df.columns:
        if 'valor' in col.lower():
            df[col] = clean_currency(df[col])
            
    df['arquivo_origem'] = 'Controle.xlsx'
    
    # IMPORTANTE: Para o Pix, usamos 'replace' para garantir que a tabela reflita o Excel atual
    df.to_sql('payment_pix', engine, schema='postgres_raw', if_exists='replace', index=False)
    print(f"✅ {len(df)} registros de Pix enviados para postgres_raw.")


def process_combustivel():
    path = "/home/ricardo/study/statistic/data/raw/Controle.xlsx"
    # Carrega a aba de consumo do Nissan Kicks
    df = pd.read_excel(path, sheet_name='nissan_kicks_consumption')
    df = df.dropna(how='all')
    
    # Limpeza básica de valores numéricos (se houver colunas de valor/litros)
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['valor', 'litro', 'km', 'preço']):
            df[col] = clean_currency(df[col])
            
    df['arquivo_origem'] = 'Controle.xlsx'
    df.to_sql('nissan_kicks_consumption', engine, schema='postgres_raw', if_exists='replace', index=False)
    print(f"✅ Aba de combustível carregada em postgres_raw.")

def process_investimentos():
    path = "/home/ricardo/study/statistic/data/raw/Controle.xlsx"
    # Carrega a aba de movimentos de estoque/ações
    df = pd.read_excel(path, sheet_name='stock_movements')
    df = df.dropna(how='all')
    
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['valor', 'preço', 'quantidade', 'taxa']):
            df[col] = clean_currency(df[col])
            
    df['arquivo_origem'] = 'Controle.xlsx'
    df.to_sql('stock_movements', engine, schema='postgres_raw', if_exists='replace', index=False)
    print(f"✅ Aba de investimentos carregada em postgres_raw.")

# 5. EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    # 1. CRIAÇÃO DO SCHEMA (FORÇADA)
    try:
        # Usamos connect() em vez de begin() para garantir o commit imediato
        with engine.connect() as conn:
            print("🏗️ Criando schema 'postgres_raw' caso não exista...")
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS postgres_raw;"))
            conn.commit() # Importante para garantir que o schema esteja disponível para os próximos passos
            
            print("🧹 Limpando tabela de cartão...")
            try:
                conn.execute(text("TRUNCATE TABLE postgres_raw.pagamento_cartao RESTART IDENTITY;"))
                conn.commit()
            except Exception:
                print("ℹ️ Tabela pagamento_cartao ainda não existe. Será criada no upload.")
    except Exception as e:
        print(f"⚠️ Aviso na preparação do banco: {e}")

    process_pagamento_dinheiro()
    process_pagamento_cartao()
    process_combustivel()      # Nova
    process_investimentos()    # Nova

    print("\n🚀 Carga completa: Finanças, Consumo e Investimentos!")

    # 2. CARGA DOS DADOS
    # Agora o schema 'postgres_raw' JÁ EXISTE, então o to_sql vai funcionar
    try:
        process_pagamento_dinheiro()
    except Exception as e:
        print(f"❌ Erro no Pix: {e}")

    try:
        process_pagamento_cartao()
    except Exception as e:
        print(f"❌ Erro no Cartão: {e}")

    print("\n🚀 Carga finalizada!")