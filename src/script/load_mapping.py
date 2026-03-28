import json
import pandas as pd
from sqlalchemy import create_engine, text
import os

# Database Connection String
# Format: postgresql://user:password@host:port/database
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'

def load_merchant_mappings():
    """
    Reads the description.json file and syncs it with the PostgreSQL 
    database using an UPSERT logic.
    """
    engine = create_engine(DB_URL)
    # This looks for the file one level up from the 'script' folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.abspath(os.path.join(current_dir, '..', 'description.json'))
    
    if not os.path.exists(json_path):
        print(f"❌ Error: File not found at {json_path}")
        return

    # 1. Extraction
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 2. Transformation (Normalizing column names to match DB)
    df = pd.DataFrame(raw_data)
    df = df.rename(columns={
        'original': 'original_description', 
        'new': 'mapped_category'
    })

    # DEDUPLICATION: Ensures each merchant appears only once
    # This prevents the 'CardinalityViolation' error in Postgres
    df = df.drop_duplicates(subset=['original_description'], keep='last')

    # 3. Loading (Using a temporary table for the UPSERT)
    print("⏳ Synchronizing local JSON with Database...")
    
    try:
        # Load data to a staging table
        df.to_sql('stg_merchant_mapping', engine, if_exists='replace', index=False)

        with engine.begin() as conn:
            # SQL Upsert: Insert new records or update existing ones
            upsert_query = text("""
                INSERT INTO dim_merchant_mapping (original_description, mapped_category)
                SELECT original_description, mapped_category FROM stg_merchant_mapping
                ON CONFLICT (original_description) 
                DO UPDATE SET 
                    mapped_category = EXCLUDED.mapped_category,
                    updated_at = CURRENT_TIMESTAMP;
            """)
            conn.execute(upsert_query)
            
            # Clean up the staging table
            conn.execute(text("DROP TABLE stg_merchant_mapping;"))
            
        print("✅ Success! Database table 'dim_merchant_mapping' is up to date.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    load_merchant_mappings()