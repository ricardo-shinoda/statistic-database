import psycopg2
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Conexão com o seu banco statistic_db no Docker
conn = psycopg2.connect(
    host= os.getenv('DB_HOST'),
    database= os.getenv('DB_NAME'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASS')  
)
cursor = conn.cursor()

cursor.execute("""
    SELECT DISTINCT ticker 
    FROM postgres_raw.stock_movements 
    WHERE ticker NOT IN ('CDB', 'Dolar') AND ticker IS NOT NULL;
""")
tickers = [row[0] for row in cursor.fetchall()]

# 3. Garante que a tabela de preços atuais existe no schema de staging/raw
cursor.execute("""
    CREATE TABLE IF NOT EXISTS postgres_raw.current_prices (
        ticker VARCHAR(10) PRIMARY KEY,
        current_price NUMERIC(10, 2),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

print(f"Atualizando preços para os tickers: {tickers}")

# 4. Dicionário de tradução e tratamento de exceções de mercado
ticker_mapping = {
    'Bitcoin': 'BTC-BRL',
    'ETH': 'ETH-BRL',
    'B3': 'B3SA3',
    'VIIA3': 'BHIA3', 
    'MALL11': 'BTLG11',
    'AESB3': 'AURE3'
}

# Lista de falsos tickers que devem ser completamente ignorados
ignore_list = ['Emolumentos', 'IRRS s/ operações', 'IRFR s/ operações', 'Taxa Liquidação']

print(f"Atualizando preços para os tickers: {tickers}")

for ticker in tickers:
    if ticker in ignore_list or ticker is None:
        continue
        
    try:
        if ticker in ticker_mapping:
            yahoo_ticker = ticker_mapping[ticker]
        else:
            yahoo_ticker = f"{ticker}.SA" if not ticker.endswith('.SA') else ticker
        
        ticker_data = yf.Ticker(yahoo_ticker)
        price = ticker_data.fast_info['last_price']
        
        if price is not None and price > 0:
            cursor.execute("""
                INSERT INTO postgres_raw.current_prices (ticker, current_price, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ticker) 
                DO UPDATE SET current_price = EXCLUDED.current_price, updated_at = CURRENT_TIMESTAMP;
            """, (ticker, price))
            
            print(f"✅ {ticker} (no Yahoo como {yahoo_ticker}): R$ {price:.2f}")
        else:
            print(f"⚠️ {ticker}: Preço retornado é inválido.")
            
    except Exception as e:
        print(f"❌ Erro ao atualizar {ticker}: {e}")

conn.commit()
cursor.close()
conn.close()
print("🎉 Todos os preços foram atualizados no Postgres!")