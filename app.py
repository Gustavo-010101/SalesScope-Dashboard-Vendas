import streamlit as st
import pandas as pd
import plotly.express as px
from database import load_sales

st.set_page_config(page_title='SalesScope | Dashboard de Vendas', page_icon='📊', layout='wide')
BG, PANEL, GOLD, TEXT = '#090d16', '#151c2a', '#e8bb59', '#f5f3eb'

st.markdown('''<style>
.stApp,[data-testid="stAppViewContainer"] {background:#090d16;color:#f5f3eb;}
[data-testid="stSidebar"] {background:#111827;border-right:1px solid #343041;}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] h2 {color:#f5f3eb!important;}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] input,
[data-testid="stSidebar"] [data-baseweb="select"] input {background:#202a3a!important;color:#f5f3eb!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] {background:#8c6a29!important;}
[data-testid="stSidebar"] [data-baseweb="tag"] span {color:#fff!important;}
[data-testid="stMetric"] {background:#151c2a;padding:16px;border-radius:15px;border:1px solid #383447;min-width:0;}
[data-testid="stMetricLabel"] * {color:#c7cbd5!important;}
[data-testid="stMetricValue"] {min-width:0;}
[data-testid="stMetricValue"] * {color:#e8bb59!important;font-size:clamp(1.15rem,1.65vw,1.75rem)!important;letter-spacing:-.02em;}
h1,h2,h3 {color:#f5f3eb!important;}
[data-testid="stCaptionContainer"] {color:#a9b2c3;}
[data-testid="stDownloadButton"] button {background:#e8bb59;color:#12151c;border:0;font-weight:700;}
</style>''', unsafe_allow_html=True)

@st.cache_data(ttl=300)
def fetch_data():
    return load_sales()

def brl(value):
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def compact_brl(value):
    a = abs(value)
    if a >= 1_000_000:
        return f'R$ {value/1_000_000:.2f} mi'.replace('.', ',')
    if a >= 10_000:
        return f'R$ {value/1_000:.1f} mil'.replace('.', ',')
    return brl(value)

def pct(value):
    return f'{value:+.1f}%'.replace('.', ',')

def chart(fig, money_axis=None):
    fig.update_layout(template='plotly_dark',paper_bgcolor=PANEL,plot_bgcolor=PANEL,
        font=dict(color=TEXT),margin=dict(l=12,r=12,t=25,b=20),
        colorway=[GOLD],hoverlabel=dict(bgcolor='#252e40',font_color=TEXT),
        xaxis=dict(gridcolor='#30394a',zerolinecolor='#30394a'),
        yaxis=dict(gridcolor='#30394a',zerolinecolor='#30394a'),height=340,
        legend_title_text='')
    if money_axis:
        fig.update_layout(**{f'{money_axis}axis_tickprefix':'R$ ',f'{money_axis}axis_tickformat':',.2s'})
    return fig

st.title('📊 SalesScope — Painel de Vendas')
st.caption('Inteligência comercial • Python + MySQL • Dados demonstrativos fictícios')
try:
    df = fetch_data()
except Exception as exc:
    st.error('Não foi possível conectar ao MySQL. Confira o .env e a tabela sales.')
    st.exception(exc)
    st.stop()
if df.empty:
    st.warning('O banco está vazio. Execute generate_data.py para inserir os pedidos demonstrativos.')
    st.stop()

for col in ['quantity','unit_price','unit_cost']:
    df[col] = pd.to_numeric(df[col],errors='coerce')
df['order_date'] = pd.to_datetime(df['order_date'],errors='coerce')
df = df.dropna(subset=['order_date','quantity','unit_price','unit_cost']).copy()
if df.empty:
    st.error('Nenhum registro válido disponível.')
    st.stop()
df['revenue'] = df['quantity'] * df['unit_price']
df['profit'] = df['quantity'] * (df['unit_price']-df['unit_cost'])

st.sidebar.header('⚙️ Filtros')
min_date,max_date = df['order_date'].min().date(),df['order_date'].max().date()
period = st.sidebar.date_input('Período',value=(min_date,max_date),min_value=min_date,max_value=max_date,format='DD/MM/YYYY')
category_options = sorted(df['category'].dropna().unique().tolist())
state_options = sorted(df['state'].dropna().unique().tolist())
categories = st.sidebar.multiselect('Categorias',category_options,default=category_options)
states = st.sidebar.multiselect('Estados',state_options,default=state_options)
if not isinstance(period,(tuple,list)) or len(period)!=2:
    st.info('Selecione as datas inicial e final.')
    st.stop()
start,end = period
segment = df.loc[df['category'].isin(categories)&df['state'].isin(states)].copy()
filtered = segment.loc[segment['order_date'].dt.date.between(start,end)].copy()
if filtered.empty:
    st.warning('Nenhuma venda encontrada para os filtros selecionados.')
    st.stop()

revenue = filtered['revenue'].sum()
profit = filtered['profit'].sum()
orders = filtered['order_id'].nunique()
margin = profit/revenue*100 if revenue else 0
prev_end = start-pd.Timedelta(days=1)
prev_start = prev_end-pd.Timedelta(days=(end-start).days)
previous = segment.loc[segment['order_date'].dt.date.between(prev_start,prev_end)]
prev_revenue = previous['revenue'].sum()
change = (revenue/prev_revenue-1)*100 if prev_revenue else None

st.subheader('Visão geral')
a,b,c,d = st.columns(4)
a.metric('Faturamento',compact_brl(revenue),delta=pct(change) if change is not None else None,
         help=f'Valor exato: {brl(revenue)}. Variação contra período anterior de igual duração, com os mesmos filtros.')
b.metric('Lucro bruto estimado',compact_brl(profit),help=f'Valor exato: {brl(profit)}')
c.metric('Pedidos',f'{orders:,}'.replace(',','.'))
d.metric('Ticket médio',compact_brl(revenue/orders if orders else 0),help=f'Valor exato: {brl(revenue/orders if orders else 0)}')
st.caption(f'Faturamento exato: {brl(revenue)} • Lucro exato: {brl(profit)} • Margem bruta: {margin:.1f}%'.replace(f'{margin:.1f}%',f'{margin:.1f}%'.replace('.',',')))
if change is None:
    st.info('Comparação com o período anterior indisponível: não há faturamento no intervalo anterior de igual duração para os filtros atuais.')
else:
    st.caption(f'Comparação com período anterior ({prev_start:%d/%m/%Y} a {prev_end:%d/%m/%Y}): {pct(change)} de faturamento.')

monthly = (filtered.assign(month=filtered['order_date'].dt.to_period('M').dt.to_timestamp())
           .groupby('month',as_index=False).agg(revenue=('revenue','sum'),profit=('profit','sum')))
by_category = filtered.groupby('category',as_index=False)['revenue'].sum().sort_values('revenue',ascending=False)
by_state = filtered.groupby('state',as_index=False)['revenue'].sum().sort_values('revenue',ascending=False)
by_product = (filtered.groupby('product',as_index=False)
              .agg(revenue=('revenue','sum'),profit=('profit','sum'),units=('quantity','sum'))
              .sort_values('revenue',ascending=False))

left,right=st.columns([3,2])
with left:
    st.subheader('Evolução mensal do faturamento')
    fig=px.line(monthly,x='month',y='revenue',markers=True,labels={'month':'Mês','revenue':'Faturamento'})
    fig.update_traces(line_color=GOLD,marker_color=GOLD)
    st.plotly_chart(chart(fig,'y'),use_container_width=True)
with right:
    st.subheader('Faturamento por categoria')
    fig=px.bar(by_category,x='category',y='revenue',labels={'category':'Categoria','revenue':'Faturamento'},color_discrete_sequence=[GOLD])
    st.plotly_chart(chart(fig,'y'),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader('Vendas por estado')
    fig=px.bar(by_state,x='state',y='revenue',labels={'state':'UF','revenue':'Faturamento'},color_discrete_sequence=[GOLD])
    st.plotly_chart(chart(fig,'y'),use_container_width=True)
with right:
    st.subheader('Produtos com maior lucro bruto')
    top_profit=by_product.sort_values('profit',ascending=False).head(8)
    fig=px.bar(top_profit,x='profit',y='product',orientation='h',labels={'profit':'Lucro bruto (R$)','product':'Produto'},color_discrete_sequence=[GOLD])
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(chart(fig,'x'),use_container_width=True)

st.subheader('Crescimento mensal')
monthly_growth=monthly.copy()
monthly_growth['Crescimento (%)']=monthly_growth['revenue'].pct_change()*100
monthly_growth['Mês']=monthly_growth['month'].dt.strftime('%m/%Y')
st.dataframe(monthly_growth[['Mês','revenue','profit','Crescimento (%)']].rename(columns={'revenue':'Faturamento (R$)','profit':'Lucro bruto (R$)'}),hide_index=True,use_container_width=True,
    column_config={'Faturamento (R$)':st.column_config.NumberColumn(format='%.2f'),
                   'Lucro bruto (R$)':st.column_config.NumberColumn(format='%.2f'),
                   'Crescimento (%)':st.column_config.NumberColumn(format='%.1f%%')})
st.caption('Crescimento mensal calculado entre meses consecutivos presentes no filtro. Meses parciais podem distorcer a comparação.')

st.subheader('Ranking de produtos')
ranking=by_product.rename(columns={'product':'Produto','revenue':'Faturamento (R$)','profit':'Lucro bruto (R$)','units':'Unidades'})
st.dataframe(ranking,hide_index=True,use_container_width=True,column_config={
    'Faturamento (R$)':st.column_config.NumberColumn(format='%.2f'),
    'Lucro bruto (R$)':st.column_config.NumberColumn(format='%.2f')})

st.subheader('Pedidos detalhados')
export=filtered[['order_date','order_id','product','category','state','quantity','unit_price','unit_cost','revenue','profit']].sort_values('order_date',ascending=False)
labels={'order_date':'Data','order_id':'Pedido','product':'Produto','category':'Categoria',
        'state':'UF','quantity':'Quantidade','unit_price':'Preço unitário (R$)',
        'unit_cost':'Custo unitário (R$)','revenue':'Faturamento (R$)','profit':'Lucro bruto (R$)'}
display=export.rename(columns=labels)
st.dataframe(display,hide_index=True,use_container_width=True,height=370,
    column_config={'Data':st.column_config.DatetimeColumn(format='DD/MM/YYYY')})
st.download_button('⬇️ Exportar CSV',data=display.to_csv(index=False,sep=';',decimal=',').encode('utf-8-sig'),
                   file_name='salesscope_vendas_filtradas.csv',mime='text/csv')
st.caption('Lucro bruto estimado = faturamento menos custo dos produtos. Não inclui impostos, frete ou despesas operacionais.')
