import os
from pathlib import Path
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Encontra a raiz do projeto dinamicamente a partir deste script
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / '.env'

# Carrega o arquivo .env apontando para o caminho absoluto correto
load_dotenv(dotenv_path=ENV_PATH)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Se as variáveis cruciais vierem vazias, mata o processo antes de tentar o banco
if not db_user or not db_password:
    raise ValueError(f"Erro: DB_USER ou DB_PASSWORD não foram encontrados no arquivo .env carregado em: {ENV_PATH}")

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_string)

query = """
SELECT
    initcap(m.investor) as investor,
    m.month as mes_competencia,
    round(sum(m.total_amount)::numeric, 2) as total_dividendos
FROM postgres_raw.stock_movements m
WHERE trim(lower(m.investor)) in ('lucas', 'luísa', 'ricardo', 'casa')
  AND trim(lower(m.transaction_type)) in ('dividendo', 'juros sobre capital', 'rendimento', 'rendimento (dividendo)', 'provento frações')
GROUP BY 1, 2
"""

df = pd.read_sql(query, engine)

# 🛠️ A MÁGICA ESTÁ AQUI: Transforma a data em texto no formato 'Ano-Mês' (ex: 2026-03)
df['mes_competencia'] = pd.to_datetime(df['mes_competencia']).dt.strftime('%Y-%m')
df = df.sort_values('mes_competencia')

# Gera o gráfico com o eixo X agora perfeitamente categorizado
fig = px.bar(
    df, 
    x='mes_competencia', 
    y='total_dividendos', 
    color='investor',
    title='Evolução de Recebimento de Dividendos por Investidor',
    labels={'mes_competencia': 'Mês de Competência', 'total_dividendos': 'Total (R$)', 'investor': 'Investidor'},
    barmode='group'  # Mantém as barras de cada investidor lado a lado dentro do respectivo mês
)

# Ajuste opcional para deixar o layout do eixo X limpo e legível
fig.update_layout(xaxis_type='category')

fig.show()