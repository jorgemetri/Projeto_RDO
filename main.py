import streamlit as st
import os

st.set_page_config(page_title="RDO", page_icon=":bar_chart:", layout="wide")

# Caminho relativo a partir do main.py
estatistica = st.Page("Estatísticas/estatistica.py", 
                         title="Estatística", 
                         icon=":material/dashboard:")

analise = st.Page("Análise/analise.py",     
                         title="Análise", 
                         icon=":material/dashboard:")

pg = st.navigation({ "Análise": [analise],"Estatistica": [estatistica]})
pg.run()