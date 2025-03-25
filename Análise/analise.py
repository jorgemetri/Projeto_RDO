import streamlit as st
import datetime
from services.verificacao import Verificar_entrada
from services.pegar_dados import ExecutarAnalise,CorrigirDados,ValidaDatas,salvar_dataframe_em_excel
import pandas as pd

if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = {}
# Título da página
st.title("Análise")

# Criando Tabs: Upar dados, Baixar dados
upar, baixar = st.tabs(["⬆️ Upar dados", "⬇️ Baixar dados"])

# Tab "Upar dados"
with upar:
    st.header("Selecione o intervalo de tempo")

    # Criando um slider para selecionar o intervalo de tempo
    try:
        # Usando st.date_input com um tuple para definir o intervalo
        date_range = st.date_input(
            "Selecione o intervalo de tempo",
            value=(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)),
            min_value=datetime.date(2020, 1, 1),
            max_value=datetime.date(2030, 12, 31),
            format="DD/MM/YYYY"
        )

        # Verifica se o usuário selecionou um intervalo válido (dois valores)
        if len(date_range) == 2:
            data_inicial, data_final = date_range
            st.success('Data e Fim selecionado!')
        else:
            st.error("Por favor, selecione uma data de início e uma data de fim.")
            data_inicial, data_final = None, None
    except Exception as e:
        st.error(f"Erro ao selecionar o intervalo de tempo: {str(e)}")
        data_inicial, data_final = None, None

    st.divider()

    st.header("Selecione o arquivo")
    arquivo = st.file_uploader("Clique em Browse Files", type=["xlsx", "xls"])

    # Exibe o nome do arquivo, se selecionado
    if arquivo is not None:
        st.write(f"Arquivo selecionado: {arquivo.name}")
        df_acesso = pd.read_excel(arquivo, engine='openpyxl')
        
    else:
        st.write("Nenhum arquivo selecionado.")
    
    
    # Botão para executar a análise
    if st.button("Executar Análise"):
        # Verifica se todas as entradas são válidas antes de prosseguir
        if data_inicial is None or data_final is None:
            st.error("Selecione um intervalo de tempo válido antes de executar a análise.",icon="🚨")
        elif arquivo is None:
            st.error("Selecione um arquivo antes de executar a análise.")
        elif not ValidaDatas(df_acesso,data_inicial,data_final):
            st.error("O intervalo de data fornecido não corresponde ao intervalo da tabela fornecida",icon="🚨")
        else:
            # Verificar se o arquivo é o arquvio no formato correto:
            with st.spinner('Aguardando enquanto está analisando...'):
                df_acesso['DT Acesso'] = df_acesso['DT Acesso'].dt.date
                df_acesso =ExecutarAnalise(df_acesso,data_inicial,data_final)
                st.write(df_acesso)
                st.session_state['dataframe']= df_acesso
            st.success("Feito!")
            

# Tab "Baixar dados"
with baixar:
    st.header("Baixar dados")
    st.divider()

    # Adicionando funcionalidade para baixar dados
    st.write("Selecione o formato para baixar os dados:")

    # Exemplo: botão para baixar um arquivo de exemplo
    formato = st.selectbox("Formato", ["CSV", "Excel"])
    
    # Simulando dados para download (substitua por seus dados reais)
    dados_exemplo = pd.DataFrame({
        "Coluna1": [1, 2, 3],
        "Coluna2": ["A", "B", "C"]
    })

    if formato == "Excel":
        # Verifica se 'dataframe' existe no session_state e se não está vazio
        if 'dataframe' in st.session_state and not st.session_state['dataframe'].empty:
            try:
                # Verifica se o DataFrame é válido
                df = st.session_state['dataframe']
                if not isinstance(df, pd.DataFrame):
                    raise ValueError("O objeto em st.session_state['dataframe'] não é um DataFrame válido.")
                
                # Tenta converter o DataFrame para Excel
                buffer = salvar_dataframe_em_excel(df)
                if buffer is None:
                    raise ValueError("A função salvar_dataframe_em_excel retornou None.")
                
                # Fornece o buffer para download
                st.download_button(
                    label="Baixar dados como Excel",
                    data=buffer,
                    file_name="dados_acesso.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Erro ao gerar o arquivo Excel: {e}")
    else:
        st.warning("Nenhum dado disponível para download em Excel.")