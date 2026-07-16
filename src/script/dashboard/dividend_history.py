import pandas as pd
import plotly.express as px
import locale
from src.script.utils import get_database_engine

engine = get_database_engine()

query = """
SELECT
    initcap(m.investor) as investor,
    m.month as mes_competencia,
    round(sum(m.total_amount)::numeric, 2) as total_dividendos
FROM postgres_raw.investments m
WHERE trim(lower(m.investor)) in ('lucas', 'luísa', 'ricardo', 'casa')
  AND trim(lower(m.transaction_type)) in ('dividendo', 'juros sobre capital', 'rendimento', 'rendimento (dividendo)', 'provento frações')
GROUP BY 1, 2
"""

df = pd.read_sql(query, engine)

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'pt_BR')

df['data_aux'] = pd.to_datetime(df['mes_competencia'], format='%Y-%m')
df = df.sort_values('data_aux')

df['mes_competencia'] = df['data_aux'].dt.strftime('%Y-%m')

fig = px.bar(
    df, 
    x='mes_competencia', 
    y='total_dividendos', 
    color='investor',
    title='Evolução de Recebimento de Dividendos por Investidor',
    labels={'mes_competencia': 'Mês de Competência', 'total_dividendos': 'Total (R$)', 'investor': 'Investidor'},
    barmode='group',
    text='total_dividendos',
    width=3000,
    height=800
)

fig.update_traces(
    texttemplate='R$ %{text:.2f}',  
    textposition='outside',         
    cliponaxis=False,               
    textangle=-90,                  
    textfont=dict(size=10, color='black'),          
    constraintext='none'            
)

fig.update_layout(
    xaxis={
        'type': 'category', 
        'categoryorder': 'category ascending',
        'tickangle': -45
    }, 
    margin=dict(t=100, b=120, l=60, r=40),
    yaxis=dict(range=[0, df['total_dividendos'].max() * 1.25]), 
    uniformtext_mode=False          
)

fig.show()