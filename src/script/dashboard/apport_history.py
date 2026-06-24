import pandas as pd
import plotly.express as px
from  src.script.utils import get_database_engine

engine = get_database_engine()

query = """
SELECT
    initcap(m.investor) as investor,
    date_trunc('month', m.transaction_date)::date as mes_competencia,
    round(
        sum(
            case 
                when trim(lower(m.transaction_type)) in ('compra', 'aporte') then abs(m.total_amount)
                else 0 
            end
        )::numeric, 2
    ) as aporte_liquido
FROM postgres_raw.investments m
WHERE trim(lower(m.investor)) in ('lucas', 'luísa', 'ricardo', 'casa')
  AND trim(lower(m.ticker)) not in ('cdi', 'cdb')
  AND trim(lower(m.transaction_type)) not like 'calculo ir%%'
GROUP BY 1, 2
"""

df = pd.read_sql(query, engine)
print(df[df['mes_competencia'].astype(str).str.contains('2026-06')])

# 1. Making sure Pandas will not treat data as text
df['mes_competencia'] = pd.to_datetime(df['mes_competencia'])
df = df.sort_values('mes_competencia')

# 2. Plot the graph
fig = px.line(
    df, 
    x='mes_competencia', 
    y='aporte_liquido', 
    color='investor',
    title='Evolucao de Aportes Mensais por Investidor',
    labels={'mes_competencia': 'Mes de Competencia', 'aporte_liquido': 'Aporte Liquido (R$)', 'investor': 'Investidor'},
    markers=True
)

# 3. Forces the X-axis to display as Year-Month while preserving the correct linear time scale
fig.update_layout(
    xaxis={
        'type': 'date',
        'dtick': 'M1',        # Month to month
        'tickformat': '%Y-%m', # Clean label
        'tickangle': -90       # Rotationing
    }
)

fig.show()