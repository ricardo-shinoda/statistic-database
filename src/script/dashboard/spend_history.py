import pandas as pd
import plotly.express as px
import psycopg2
import sys
from src.script.utils import get_database_engine

engine = get_database_engine()

# def carregar_dados_do_postgres():
#     """
#     Conecta ao banco local PostgreSQL e traz os dados da fct_unified_payments.
#     """
#     try:
#         # Ajuste as credenciais conforme o seu ambiente Docker/local
#         conn = get_database_engine()
        
#         # Query ajustada para as suas colunas reais
#         # Filtra para trazer apenas transações de pagamento reais e remove transferências internas
#         query = """
#             SELECT 
#                 purchased_at,
#                 amount_brl,
#                 payment_type,
#                 category_name
#             FROM analytics.fct_unified_payments
#             WHERE is_payment_transaction = TRUE
#               AND is_internal_transfer = FALSE
#               AND amount_brl > 0
#         """
#         df = pd.read_sql(query, conn)
#         return df
#     except Exception as e:
#         print(f"Erro ao conectar ou ler dados do PostgreSQL: {e}")
#         sys.exit(1)

def carregar_dados_do_postgres():
    """
    Conecta ao banco local PostgreSQL e traz os dados reais de gastos da fct_unified_payments.
    """
    try:
        engine = get_database_engine()
        
        # Ajustamos os filtros com base no comportamento real dos dados:
        # Pega apenas o que não for transferência entre suas contas e que tenha valor de gasto real (> 0)
        query = """
            SELECT 
                purchased_at,
                amount_brl,
                payment_type,
                category_name
            FROM analytics.fct_unified_payments
            WHERE is_internal_transfer = FALSE
              AND amount_brl > 0
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Erro ao conectar ou ler dados do PostgreSQL: {e}")
        sys.exit(1)

def gerar_dashboard_gastos():
    df = carregar_dados_do_postgres()
    
    if df.empty:
        print("Nenhum dado encontrado com os filtros aplicados.")
        return

    # --- TRATAMENTO ---
    # Garante que a categoria comece com letra maiúscula para o gráfico
    df['category_name'] = df['category_name'].fillna('Não Categorizado').str.strip().str.capitalize()
    
    # Padroniza o nome do tipo de pagamento (PIX, Credit Card, etc.)
    df['payment_type'] = df['payment_type'].fillna('Outros').str.strip().str.upper()
    
    # Agrupa por categoria e tipo de pagamento para consolidar os valores do gráfico
    df_agrupado = df.groupby(['category_name', 'payment_type'], as_index=False)['amount_brl'].sum()
    df_agrupado = df_agrupado.sort_values(by='amount_brl', ascending=False)

    # --- GRÁFICO ---
    fig = px.bar(
        df_agrupado,
        x='category_name',
        y='amount_brl',
        color='payment_type',
        title='Distribuição de Gastos por Categoria e Meio de Pagamento',
        labels={'category_name': 'Categoria', 'amount_brl': 'Total Gasto (R$)', 'payment_type': 'Meio de Pagamento'},
        barmode='group', # Mantém as barras de Pix/Cartão lado a lado por categoria
        text='amount_brl',
        width=1500,
        height=800
    )

    # Rótulos de dados verticais e sem o corte teimoso do Plotly
    fig.update_traces(
        texttemplate='R$ %{text:.2f}',
        textposition='outside',
        cliponaxis=False,
        textangle=-90,
        textfont=dict(size=10, color='black'),
        constraintext='none'
    )

    # Ajustes de layout para o eixo X respirar sem encavalar os nomes
    fig.update_layout(
        xaxis={
            'type': 'category',
            'categoryorder': 'total descending', # Maior gasto da esquerda para a direita
            'tickangle': -45
        },
        margin=dict(t=100, b=140, l=70, r=40),
        yaxis=dict(range=[0, df_agrupado['amount_brl'].max() * 1.30]), # Folga para o texto vertical
        uniformtext_mode=False
    )

    fig.show()

if __name__ == "__main__":
    gerar_dashboard_gastos()