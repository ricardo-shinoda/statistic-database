import json
import pandas as pd
from sqlalchemy import create_engine, text
import os

# Database Connection String
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'

def load_merchant_mappings():
    engine = create_engine(DB_URL)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.abspath(os.path.join(current_dir, '..', 'description.json'))
    
    if not os.path.exists(json_path):
        print(f"❌ Erro: Arquivo não encontrado em {json_path}")
        return

    # --- 1. EXTRACTION ---
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # --- 2. TRANSFORMATION (Pandas) ---
    df = pd.DataFrame(raw_data)
    
    # Renaming for a clean database naming standard
    rename_map = {
        'original': 'original_description', 
        'categoria': 'mapped_category',
        'subcategoria': 'mapped_subcategory'
    }
    df = df.rename(columns=rename_map)

    # Deduplicating to ensure data integrity
    df = df.drop_duplicates(subset=['original_description'], keep='last')

    # --- 3. LOADING (Adapted for ELT/dbt Workflow) ---
    print("⏳ Sincronizando mapeamentos com o schema postgres_raw...")
    
    try:
        required_cols = ['original_description', 'mapped_category', 'mapped_subcategory']
        df[required_cols].to_sql(
            'merchant_categories', 
            engine, 
            schema='postgres_raw',
            if_exists='replace', 
            index=False
        )

        print("✅ Sucesso! Tabela 'postgres_raw.merchant_categories' atualizada.")
        print("💡 Agora o dbt pode usar esta tabela para categorizar suas faturas.")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a carga: {e}")

if __name__ == "__main__":
    load_merchant_mappings()