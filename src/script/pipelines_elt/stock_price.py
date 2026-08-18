import yfinance as yf
from src.script.utils import get_database_engine
from sqlalchemy import text

engine = get_database_engine()

with engine.begin() as conn:

    query_tickers = text("""
        SELECT DISTINCT ticker 
        FROM postgres_raw.stock_movements 
        WHERE ticker NOT IN ('CDB') AND ticker IS NOT NULL;
    """)
    result_tickers = conn.execute(query_tickers)
    tickers = [row[0] for row in result_tickers.fetchall()]

    create_table_query = text("""
        CREATE TABLE IF NOT EXISTS postgres_raw.current_prices (
            ticker VARCHAR(10) PRIMARY KEY,
            current_price NUMERIC(10, 2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.execute(create_table_query)

    print(f"Atualizando preços para os tickers: {tickers}")

    ticker_mapping = {
        'Bitcoin': 'BTC-BRL',
        'ETH': 'ETH-BRL',
        'B3': 'B3SA3',
        'VIIA3': 'BHIA3', 
        'MALL11': 'BTLG11',
        'AESB3': 'AURE3',
        'Dolar': 'BRL=X'
    }

    ignore_list = ['Emolumentos', 'IRRS s/ operações', 'IRFR s/ operações', 'Taxa Liquidação']

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
                insert_query = text("""
                    INSERT INTO postgres_raw.current_prices (ticker, current_price, updated_at)
                    VALUES (:ticker, :price, CURRENT_TIMESTAMP)
                    ON CONFLICT (ticker) 
                    DO UPDATE SET current_price = EXCLUDED.current_price, updated_at = CURRENT_TIMESTAMP;
                """)
                
                conn.execute(insert_query, {"ticker": ticker, "price": price})
                
                print(f"✅ {ticker} (no Yahoo como {yahoo_ticker}): R$ {price:.2f}")
            else:
                print(f"⚠️ {ticker}: Preço retornado é inválido.")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar {ticker}: {e}")

print("🎉 Todos os preços foram atualizados no Postgres!")