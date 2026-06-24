import pandas as pd
import plotly.express as px
from src.script.utils import get_database_engine

engine = get_database_engine()

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

df['mes_competencia'] = pd.to_datetime(df['mes_competencia']).dt.strftime('%Y-%m')
df = df.sort_values('mes_competencia')

# Renders the chart with a perfectly categorized X-axis
fig = px.bar(
    df, 
    x='mes_competencia', 
    y='total_dividendos', 
    color='investor',
    title='Evolução de Recebimento de Dividendos por Investidor',
    labels={'mes_competencia': 'Mês de Competência', 'total_dividendos': 'Total (R$)', 'investor': 'Investidor'},
    barmode='group'
)

# Optional formatting to ensure a clean and readable X-axis
fig.update_layout(xaxis_type='category')

fig.show()