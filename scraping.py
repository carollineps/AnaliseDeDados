import streamlit as st
import pandas as pd 

dados = pd.read_excel("Dados.xlsx")
print(dados)

st.title("Análise de Dados")
st.subheader("Comparativos dos notebooks mais vendidos do mercado livre")
st.write("Quantidade de empresas analisadas", dados["FABRICANTE"].nunique())

st.sidebar.title("Filtro")

fabricantes = st.sidebar.multiselect("Empresas", dados["FABRICANTE"].unique())

if fabricantes: 
    dados = dados[dados["FABRICANTE"].isin(fabricantes)]

st.metric("TOTAL RECEITA BRUTA", f"R${dados["TOTAL"].sum():,.2f}")
st.metric("MÉDIA RECEITA BRUTA", f"R${dados["TOTAL"].mean():,.2f}")

st.title("Gráfico de barras")
st.write("Total de vendas em real")


import altair as alt

grafico = dados.groupby("FABRICANTE")["TOTAL"].sum().reset_index()

chart = alt.Chart(grafico).mark_bar(
    color="#FF6666"
).encode(
    x=alt.X("FABRICANTE:N", sort="-y"),
    y="TOTAL:Q"
).properties(
    background="#E5A0B8"
)

st.altair_chart(chart, use_container_width=True)


mais_vendido = dados.loc[dados ["QUANTIDADE"].idxmax()]

st.metric("Produto mais vendido", mais_vendido["PRODUTO"])

ranking = dados.groupby("FABRICANTE")["TOTAL"].sum().sort_values(ascending=False) 

st.subheader("Ranking das Empresas TOP ONE 🎖️")
st.dataframe(ranking)

st.title("Melhores avaliados no mercado")

import plotly.express as px

avaliados = dados.groupby("FABRICANTE")["AVALIACAO"].sum().sort_values(ascending=False)

fig = px.pie(
    values=avaliados.values,
    names=avaliados.index,
    title="Distribuição por Fabricante"
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Melhores preço no mercado")

st.line_chart(dados.groupby("PRODUTO")["PRECO"].sum(), color="#B85C7A")

st.markdown("""
<style>

[data-testid="stHeader"] {
    background-color: #B85C7A !important;
}


[data-testid="stToolbar"] {
    background-color: #B85C7A !important;
}

.stApp {
    background-color: #E8A0B8;
}

[data-testid="stSidebar"] {
    background-color: #B85C7A;
}


[data-testid="stSidebar"] {
    color: white !important;
}


html, body, [class*="css"] {
    font-family: Georgia, "Times New Roman", serif !important;
    color: white !important;
}


h1, h2, h3, h4, h5, h6 {
    font-family: Georgia, "Times New Roman", serif !important;
    color: white !important;
}


p, span, label, div {
    font-family: Georgia, "Times New Roman", serif !important;
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: #9F4D69 !important;
    border-color: #9F4D69 !important;
}

div[data-baseweb="select"] * {
    color: white !important;
}


input {
    background-color: #9F4D69 !important;
    color: white !important;
}


[data-testid="stMetricValue"] {
    color: white !important;
    font-family: Georgia, "Times New Roman", serif !important;
}

[data-testid="stMetricLabel"] {
    color: white !important;
    font-family: Georgia, "Times New Roman", serif !important;
}
[data-testid="stDataFrame"] {
    background-color: "rgba(0,0,0,0)" !important;
}


</style>
""", unsafe_allow_html=True)


