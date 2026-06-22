# import os
# from pathlib import Path
import pandas as pd
import plotly.express as px
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
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
FROM postgres_raw.stock_movements m
WHERE trim(lower(m.investor)) in ('lucas', 'luísa', 'ricardo', 'casa')
  AND trim(lower(m.ticker)) not in ('cdb', 'taxa liquidação', 'emolumentos', 'irrs s/ operações', 'cdi')
  AND trim(lower(m.transaction_type)) not like 'calculo ir%%'
GROUP BY 1, 2
"""

df = pd.read_sql(query, engine)

# 1. Garante que o Pandas trate a coluna como uma DATA de verdade (e nao texto)
df['mes_competencia'] = pd.to_datetime(df['mes_competencia'])
df = df.sort_values('mes_competencia')

# 2. Plota o grafico usando a linha do tempo nativa
fig = px.line(
    df, 
    x='mes_competencia', 
    y='aporte_liquido', 
    color='investor',
    title='Evolucao de Aportes Mensais por Investidor',
    labels={'mes_competencia': 'Mes de Competencia', 'aporte_liquido': 'Aporte Liquido (R$)', 'investor': 'Investidor'},
    markers=True
)

# 3. Força o formato de exibição no eixo X para Ano-Mês, mantendo a escala temporal linear correta
fig.update_layout(
    xaxis={
        'type': 'date',
        'dtick': 'M1',        # Mostra marcações de 1 em 1 mês
        'tickformat': '%Y-%m', # Garante o visual limpo '2026-03' no label
        'tickangle': -90       # Rotaciona para não encavalar
    }
)

fig.show()