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
        print(f"❌ Error: File not found at {json_path}")
        return

    # 1. Extraction
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 2. Transformation
    df = pd.DataFrame(raw_data)
    
    # Mapping the new JSON keys to our Database columns
    rename_map = {
        'original': 'original_description', 
        'categoria': 'mapped_category',
        'subcategoria': 'mapped_subcategory'
    }
    df = df.rename(columns=rename_map)

    # Deduplication
    df = df.drop_duplicates(subset=['original_description'], keep='last')

    # 3. Loading
    print("⏳ Synchronizing local JSON with Database...")
    
    try:
        # Define the columns we want to send to the DB
        required_cols = ['original_description', 'mapped_category', 'mapped_subcategory']
        
        # Staging
        df[required_cols].to_sql(
            'stg_merchant_mapping', 
            engine, 
            if_exists='replace', 
            index=False
        )

        with engine.begin() as conn:
            # SQL Upsert: Added mapped_subcategory to the logic
            upsert_query = text("""
                INSERT INTO dim_merchant_mapping (original_description, mapped_category, mapped_subcategory)
                SELECT original_description, mapped_category, mapped_subcategory FROM stg_merchant_mapping
                ON CONFLICT (original_description) 
                DO UPDATE SET 
                    mapped_category = EXCLUDED.mapped_category,
                    mapped_subcategory = EXCLUDED.mapped_subcategory,
                    updated_at = CURRENT_TIMESTAMP;
            """)
            conn.execute(upsert_query)
            conn.execute(text("DROP TABLE IF EXISTS stg_merchant_mapping;"))
            
        print("✅ Success! Database table 'dim_merchant_mapping' is up to date with Categories and Subcategories.")
        
    except Exception as e:
        print(f"❌ An error occurred during database sync: {e}")

if __name__ == "__main__":
    load_merchant_mappings()