import streamlit as st
from services.pegar_dados import verificar_arquivo_excel
import pandas as pd

st.title("Estatística")


st.divider()


# Verifica se o arquivo existe e prossegue com a análise
if verificar_arquivo_excel('AnaliseRDO.xlsx'):
    try:
        # Carrega o DataFrame
        df = pd.read_excel('AnaliseRDO.xlsx', engine='openpyxl')

        # Agrupa por 'Data RDO' e soma 'Tempo Horas Trabalhadas Excedentes'
        df_agrupado = df.groupby('Data RDO')['Tempo Horas Trabalhadas Excedentes'].sum().reset_index()

        # Exibe o DataFrame agrupado (opcional, para verificação)

        # Cria o gráfico de barras com st.bar_chart
        # st.bar_chart espera um DataFrame onde o índice é o eixo X e as colunas são os valores do eixo Y
        df_plot = df_agrupado.set_index('Data RDO')
        st.bar_chart(
            df_plot,
            y='Tempo Horas Trabalhadas Excedentes',
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro ao processar o DataFrame ou criar o gráfico: {e}")
else:
    st.error('Rode a análise novamente caso a planilha não exista.')