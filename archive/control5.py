import os
import zipfile
import shutil
import pandas as pd
from sqlalchemy import create_engine, text
from decouple import config

# --- 1. SET THE MONTH HERE ---
CURRENT_MONTH = "2021-06" 

# --- 2. CONFIGURATION & PATHS ---
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'
ZIP_PATH = "/home/ricardo/Downloads/Fatura-CPF.zip"
ZIP_PASSWORD = config('ZIP_PASSWORD')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LAKE_DIR = os.path.join(BASE_DIR, "data_lake/raw_invoices")
CONTROLE_XLSX = os.path.join(BASE_DIR, "src/Controle.xlsx")

engine = create_engine(DB_URL)

def ingest_and_archive(invoice_month):
    year = invoice_month.split('-')[0]
    target_folder = os.path.join(LAKE_DIR, year)
    os.makedirs(target_folder, exist_ok=True)
    
    if not os.path.exists(ZIP_PATH):
        print(f"ℹ️ ZIP not in Downloads. Checking Data Lake for {invoice_month}...")
        expected_in_lake = os.path.join(target_folder, f"invoice-{invoice_month}.csv")
        return expected_in_lake if os.path.exists(expected_in_lake) else None

    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        csv_name = z.namelist()[0]
        z.extract(csv_name, "/tmp", pwd=bytes(ZIP_PASSWORD, 'utf-8'))
    
    new_csv_name = f"invoice-{invoice_month}.csv"
    final_path = os.path.join(target_folder, new_csv_name)
    shutil.move(f"/tmp/{csv_name}", final_path)
    print(f"✅ Archived: {new_csv_name}")
    return final_path

def process_credit_card(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    df = df[df['Descrição'] != 'Inclusao de Pagamento    '].copy()
    df.columns = df.columns.str.strip()

    mapping_query = "SELECT original_description, mapped_category, mapped_subcategory FROM dim_merchant_mapping"
    df_map = pd.read_sql(mapping_query, engine)
    
    df = df.merge(df_map, left_on='Descrição', right_on='original_description', how='left')
    df['final_category'] = df['mapped_category'].combine_first(df['Categoria'])
    
    df_final = pd.DataFrame({
        'transaction_date': pd.to_datetime(df['Data de Compra'], dayfirst=True),
        'description': df['Descrição'],
        'category': df['final_category'],
        'subcategory': df['mapped_subcategory'],
        'amount_brl': df['Valor (em R$)'],
        'card_holder_name': df['Nome no Cartão'],
        'installment_info': df['Parcela'],
        'transaction_type': 'credit_card',
        'status': 'Liquidado',
        'source_file': os.path.basename(csv_path)
    })
    return df_final

def process_manual_bills():
    if not os.path.exists(CONTROLE_XLSX):
        return pd.DataFrame()

    try:
        xl = pd.ExcelFile(CONTROLE_XLSX)
        # Search for sheet regardless of "Pagar" or "pagar"
        target_sheet = next((s for s in xl.sheet_names if s.lower() == 'contas a pagar'), None)
        
        if not target_sheet:
            print(f"⚠️ Sheet 'Contas a Pagar' not found. Available: {xl.sheet_names}")
            return pd.DataFrame()

        df_manual = pd.read_excel(xl, sheet_name=target_sheet)
        
        # --- HYBRID CLEANING LOGIC ---
        # 1. Drop rows that are completely empty
        df_manual = df_manual.dropna(how='all')
        
        # 2. Convert 'Quanto' to numeric (handling '-' and 'R$')
        df_manual['amount'] = (
            df_manual['Quanto']
            .astype(str)
            .replace(r'[R\$\s.]', '', regex=True)
            .replace(',', '.', regex=True)
        )
        df_manual['amount'] = pd.to_numeric(df_manual['amount'], errors='coerce').fillna(0.0)
        
        # 3. Impute missing descriptions to satisfy Postgres NOT NULL
        df_manual['Descrição'] = df_manual['Descrição'].fillna('MISSING_DESCRIPTION')

        df_final = pd.DataFrame({
            'transaction_date': pd.to_datetime(df_manual['Dia']),
            'description': df_manual['Descrição'],
            'category': 'Manual Expense',
            'subcategory': None,
            'amount_brl': df_manual['amount'],
            'card_holder_name': None,
            'installment_info': 'Única',
            'transaction_type': 'manual_bill',
            'status': df_manual['Status'],
            'source_file': 'Controle.xlsx'
        })
        
        # Keep only rows that have an actual financial impact
        return df_final[df_final['amount_brl'] > 0]
        
    except Exception as e:
        print(f"⚠️ Could not process manual bills: {e}")
        return pd.DataFrame()

def run_pipeline(month):
    print(f"🚀 Starting Pipeline for {month}...")
    csv_path = ingest_and_archive(month)
    
    all_data = []
    
    # 1. CREDIT CARD: Only delete/replace if we actually have a file to upload
    if csv_path and os.path.exists(csv_path):
        df_cc = process_credit_card(csv_path)
        if not df_cc.empty:
            with engine.begin() as conn:
                # Erase old data for THIS month only
                conn.execute(text("DELETE FROM fact_transactions WHERE source_file = :file"), 
                             {"file": f"invoice-{month}.csv"})
            all_data.append(df_cc)
    else:
        print(f"ℹ️ No new CC file found. Keeping existing data for {month}.")

    # 2. MANUAL BILLS: Always replace with the current state of Excel
    df_manual = process_manual_bills()
    if not df_manual.empty:
        # Check if Coffee is being filtered
        if 'Coffee' in df_manual['description'].values or 'Coffee' in df_manual['description'].str.lower().values:
            print("☕ SUCCESS: Coffee found in the data pipeline!")
        
        with engine.begin() as conn:
            # Erase ALL manual bills to prevent duplicates
            conn.execute(text("DELETE FROM fact_transactions WHERE transaction_type = 'manual_bill'"))
        all_data.append(df_manual)

    # 3. UPLOAD
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"✨ Done! Sync complete.")

if __name__ == "__main__":
    run_pipeline(CURRENT_MONTH)