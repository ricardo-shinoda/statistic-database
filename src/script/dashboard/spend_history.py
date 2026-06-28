import pandas as pd
import plotly.express as px
import sys
from src.script.utils import get_database_engine

def carregar_dados_do_postgres():
    """
    Conecta ao banco local PostgreSQL usando a engine padronizada do utils
    e busca os gastos com quebra mensal.
    """
    try:
        # A engine só é invocada no momento em que a função roda
        engine = get_database_engine()
        
        query = """
            SELECT 
                TO_CHAR(purchased_at, 'YYYY-MM') as mes_competencia,
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
        print(f"❌ Erro ao ler dados do PostgreSQL: {e}")
        sys.exit(1)

def gerar_dashboard_gastos_mensal():
    # Print imediato para você ter certeza que o script iniciou
    print("🔄 [DEBUG] O script iniciou! Buscando dados no banco...")
    
    df = carregar_dados_do_postgres()
    
    if df is None or df.empty:
        print("⚠️ [DEBUG] O banco retornou um DataFrame vazio.")
        return

    print(f"✅ [DEBUG] {len(df)} linhas carregadas. Tratando dados...")

    # --- TRATAMENTO ---
    df['category_name'] = df['category_name'].fillna('Não Categorizado').str.strip()
    df['payment_type'] = df['payment_type'].fillna('Outros').str.strip().str.upper()
    
    # Filtra as TOP 10 categorias com maior volume histórico de gastos
    top_categories = df.groupby('category_name')['amount_brl'].sum().nlargest(10).index
    df_filtrado = df[df['category_name'].isin(top_categories)].copy()
    df_filtrado['category_name'] = df_filtrado['category_name'].str.capitalize()

    # Agrupa por Mês, Categoria e Tipo de Pagamento
    # Agrupa por Mês, Categoria e Tipo de Pagamento
    # Agrupa por Mês, Categoria e Tipo de Pagamento
    df_agrupado = df_filtrado.groupby(['mes_competencia', 'category_name', 'payment_type'], as_index=False)['amount_brl'].sum()
    
    # 1. Garante a ordenação correta no Pandas
    df_agrupado = df_agrupado.sort_values(by='mes_competencia', ascending=True)
    
    # 2. CAPTURA A LISTA ÚNICA E CRONOLÓGICA DE TODOS OS MESES DO SEU HISTÓRICO
    lista_meses_ordenada = sorted(df_agrupado['mes_competencia'].unique())

    print(f"📊 [DEBUG] Renderizando gráfico para {len(df_agrupado)} combinações de meses/categorias...")

    # --- GRÁFICO ---
    fig = px.bar(
        df_agrupado,
        x='mes_competencia',          
        y='amount_brl',
        color='payment_type',
        facet_col='category_name',     
        facet_col_wrap=1,              
        title='Evolução Mensal de Gastos por Categoria e Meio de Pagamento (Top 10 Categorias)',
        labels={'mes_competencia': 'Mês', 'amount_brl': 'Total Gasto (R$)', 'payment_type': 'Meio de Pagamento'},
        barmode='group',
        text='amount_brl',
        width=3600,
        height=320 * len(top_categories), 
        facet_row_spacing=0.06            
    )

    # Rótulos de dados compactos verticais nas barras
    fig.update_traces(
        texttemplate='R$ %{text:.0f}',    
        textposition='outside',
        cliponaxis=False,
        textangle=-90,
        textfont=dict(size=9, color='black'),
        constraintext='none'
    )

    # Ajustes de Layout e Eixos
    fig.update_layout(
        margin=dict(t=120, b=140, l=80, r=60), 
        uniformtext_mode=False
    )
    
    # Limpa o texto das anotações do topo
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(size=12, weight='bold')))
    
    # Reseta os eixos Y para ficarem independentes por categoria
    fig.update_yaxes(matches=None, showticklabels=True) 
    
    # --- AQUI ESTÁ A SOLUÇÃO DEFINITIVA PARA O EIXO X ---
    # Forçamos o tipo para 'array' e injetamos a lista ordenada como os ticks oficiais do gráfico
    fig.update_xaxes(
        showticklabels=True, 
        tickangle=-45, 
        type='category',             # <-- Mantido como 'category'
        tickmode='array',            # <-- Adicionado para aceitar os vetores abaixo
        tickvals=lista_meses_ordenada,
        ticktext=lista_meses_ordenada
    )

    print("🚀 Abrindo o dashboard definitivo no seu navegador...")
    fig.show()

# O ponto de entrada padrão que garante a execução via flag -m
if __name__ == "__main__":
    gerar_dashboard_gastos_mensal()