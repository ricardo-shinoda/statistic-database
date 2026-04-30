import os
from sqlalchemy import text
# Importamos as configurações do seu control7
from archive.control7 import engine, HISTORICAL_XLSX_DIR, LAKE_DIR, ingest_historical_file, process_credit_card

def rebuild_everything():
    # ... (todo o código anterior de limpar banco e rodar Excel/Lake) ...
    
    print("\n📝 --- INICIANDO CARGA DE DADOS MANUAIS E EXTRAS ---")

    # 1. Processar Contas Manuais (Contas a Pagar)
    from archive.control7 import process_manual_bills, process_investments, process_vehicle_consumption
    
    df_m = process_manual_bills()
    if not df_m.empty:
        # Não precisa de DELETE aqui porque o TRUNCATE no início já limpou tudo
        df_m.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"✅ {len(df_m)} contas manuais inseridas.")

    # 2. Processar Investimentos (se houver)
    df_inv = process_investments()
    if not df_inv.empty:
        df_inv.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"📈 {len(df_inv)} registros de investimentos inseridos.")

    # 3. Processar Veículo (Nissan Kicks)
    df_v = process_vehicle_consumption()
    if not df_v.empty:
        df_v.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"🚗 {len(df_v)} registros de combustível inseridos.")

    print("\n🚀 [SUCCESS] Tudo (Cartão + Manual + Investimentos) está de volta!")

if __name__ == "__main__":
    confirm = input("⚠️ Confirmar reconstrução total? (s/n): ")
    if confirm.lower() == 's':
        rebuild_everything()