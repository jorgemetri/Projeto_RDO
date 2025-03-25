import requests
import pandas as pd
from io import StringIO
import streamlit as st
import time
import io
import os
#Cria dataframe de uma string-----------------------------------------------------------------
def create_dataframe_from_string(data_str: str) -> pd.DataFrame:
    """
    Given a multi-line string with tab-separated values,
    returns a pandas DataFrame.
    """
    # Use StringIO to simulate a file-like object from the string.
    data_io = StringIO(data_str)
    # Read the data into a DataFrame, assuming tab as the delimiter.
    df = pd.read_csv(data_io, delimiter="\t")
    return df
#Corrigir Dados-------------------------------------------------------------------
"""
Essa função corrige os dados do arquivo excel, para que seja possível realizar a análise.
Adequando a tabela dada a uma tabela de referencia
"""
def CorrigirDados(df, df_referencia):
    for index, row in df.iterrows():
        if row['Nome'] in df_referencia['Nome Errado'].values:
            # Look up the correct name where 'Nome Errado' matches the current name
            correct_name = df_referencia.loc[
                df_referencia['Nome Errado'] == row['Nome'], 'Nome Correto'
            ].values[0]
            # Update the DataFrame using .at (iterrows() returns a copy, so direct assignment won't update the df)
            df.at[index, 'Nome'] = correct_name
    return df
#Pegar Obras RDO-------------------------------------------------------------------
"""
Essa função retorna um vetor de objetos obras da LMI na SAMARCO
"""
def PegarObras():
  # URL da API que você deseja acessar

  url=f'https://apiexterna.diariodeobra.app/v1/obras'

  # Fazendo a requisição GET
  headers = {
      "token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDIzMjY2MzQsImp0aSI6IjdmMzUyY2YxYjY3MDQwNDc5YTk1OTgzYWI3N2MwMjk3YjE0YmM4YzRjYTQxODkxOGRmOTU2MTljYWJkM2U2MTUzYzkzYzEwMyIsImNvZCI6ImIyODY1N2ZhN2U2OWYzODhmNjcxMzgxOWViY2U2Mzk0ZTliODIyNGEiLCJlbXByZXNhSWQiOiI2NTgyZmY2ZjA2MDVjMWYyMTEwYzE3NDIiLCJpc3MiOiJhcHAtYXBpIn0.74vzOV4gk2gYT9ay8kKqEC58LFu5yj-5TDtIgLy1yNU'
  }
  response = requests.get(url, headers=headers)

  try:
      response = requests.get(url, headers=headers)

      print("Status code:", response.status_code)
      print("Resposta bruta:", response.text)  # Para inspecionar o que está vindo

      # Somente tente converter em JSON se o status for 200 (ou conforme a API)
      if response.status_code == 200:
          print(response.content)
          return response
      else:
          print("A requisição não retornou 200. Verifique a mensagem acima.")

  except Exception as e:
      print("Ocorreu um erro ao fazer a requisição:", e)
#Pegar ID das obras-------------------------------------------------------------------
"""
Essa função retorna um vetor de ID's das obras da LMI na SAMARCO
"""
def RetornaVetorIdObras():
  obras = PegarObras()
  obras_id=[]
  for obra in obras.json():
    obras_id.append(obra['_id'])
  return obras_id
#Pegar relatorio de obras-------------------------------------------------------------------
"""
Essa função retorna todos os relatórios de uma obra a partir do ID da obra
"""
def PegarRelatoriosObra(id_obra,data_inicio='2025-02-28',data_fim='2025-02-28'):
  url=f'https://apiexterna.diariodeobra.app/v1/obras/{id_obra}/relatorios?dataInicio={data_inicio}&dataFim={data_fim}'

  # Fazendo a requisição GET
  headers = {
      "token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDIzMjY2MzQsImp0aSI6IjdmMzUyY2YxYjY3MDQwNDc5YTk1OTgzYWI3N2MwMjk3YjE0YmM4YzRjYTQxODkxOGRmOTU2MTljYWJkM2U2MTUzYzkzYzEwMyIsImNvZCI6ImIyODY1N2ZhN2U2OWYzODhmNjcxMzgxOWViY2U2Mzk0ZTliODIyNGEiLCJlbXByZXNhSWQiOiI2NTgyZmY2ZjA2MDVjMWYyMTEwYzE3NDIiLCJpc3MiOiJhcHAtYXBpIn0.74vzOV4gk2gYT9ay8kKqEC58LFu5yj-5TDtIgLy1yNU'
  }
  response = requests.get(url, headers=headers)

  try:
      response = requests.get(url, headers=headers)

      # Somente tente converter em JSON se o status for 200 (ou conforme a API)
      if response.status_code == 200:
          return response
      else:
          print("A requisição não retornou 200. Verifique a mensagem acima.")

  except Exception as e:
      print("Ocorreu um erro ao fazer a requisição:", e)
#Pegar todos os relatórios das obras-------------------------------------------------------------------
"""
Dado um vetor de id de obras essa função ira retornar um vetor no 
formato:
 [ {id_obra_1:[id_relatorio_1,id_relatorio_2,...]},{id_obra_2:[]},...,{id_obra_n:[id_relatorio_1,...]}]
"""
def PegarTodosRelatoriosObras(obras_id, data_inicio, data_fim):
    ids_relatorios_obras = []
    for obra_id in obras_id:
        if obra_id:  # Check if obra_id is not empty or None
            relatorios = PegarRelatoriosObra(obra_id, data_inicio, data_fim)
            report_ids = []
            for relatorio in relatorios.json():
                report_ids.append(relatorio['_id'])
            # Only add the dictionary if there is at least one report
            if report_ids:
                ids_relatorios_obras.append({obra_id: report_ids})
    return ids_relatorios_obras
#Visualizar Relatório---------------------------------------------------------------------------------
"""
Essa funcao dado um id de obra e id de relatório reotnar a mão de obra
"""
def VisualizarRelatorio(id_obra,id_relatorio):
  url=f'https://apiexterna.diariodeobra.app/v1/obras/{id_obra}/relatorios/{id_relatorio}'

  # Fazendo a requisição GET
  headers = {
      "token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDIzMjY2MzQsImp0aSI6IjdmMzUyY2YxYjY3MDQwNDc5YTk1OTgzYWI3N2MwMjk3YjE0YmM4YzRjYTQxODkxOGRmOTU2MTljYWJkM2U2MTUzYzkzYzEwMyIsImNvZCI6ImIyODY1N2ZhN2U2OWYzODhmNjcxMzgxOWViY2U2Mzk0ZTliODIyNGEiLCJlbXByZXNhSWQiOiI2NTgyZmY2ZjA2MDVjMWYyMTEwYzE3NDIiLCJpc3MiOiJhcHAtYXBpIn0.74vzOV4gk2gYT9ay8kKqEC58LFu5yj-5TDtIgLy1yNU'
  }
  response = requests.get(url, headers=headers)

  try:
      response = requests.get(url, headers=headers)


      # Somente tente converter em JSON se o status for 200 (ou conforme a API)
      if response.status_code == 200:
          return response
      else:
          print("A requisição não retornou 200. Verifique a mensagem acima.")

  except Exception as e:
      print("Ocorreu um erro ao fazer a requisição:", e)


#RetornarDataNumeroNomeObra--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def RetornaDataNumeroNomeObra(id_obra, id_relatorio, data_inicio='2025-02-28', data_fim='2025-02-28'):
    """
    Essa função irá, dado um id_obra e um id_relatorio, iterar por todos os relatórios de uma obra
    e pegar apenas o referente ao id, retornando um array com as seguintes informações:
      - data RDO
      - numero do relatório
      - nome da obra

    Args:
        id_obra (str): Id referente à obra.
        id_relatorio (str): Id referente ao relatório.
        data_inicio (str, opcional): Data inicial do filtro. Padrão '2025-02-28'.
        data_fim (str, opcional): Data final do filtro. Padrão '2025-02-28'.

    Returns:
        list: [ data_RDO,numero_relatorio, nome_obra] ou None se não encontrar.
    """
    # PegarRelatoriosObra deve retornar algo que, ao chamar .json(), vire uma lista de dicionários
    relatorio = PegarRelatoriosObra(id_obra, data_inicio, data_fim)
    relatorio = relatorio.json()

    for r in relatorio:
        if r['_id'] == id_relatorio:
            # Ajuste aqui para retornar: número do relatório, data, nome da obra
            return [ r['data'],r['numero'], r['obra']['nome']]

    # Caso não encontre o relatório com o id especificado
    return None
#Criando tabela de Mão de Obras----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
Essa função irá receber uma array mão de obras da forma:

[{'id_mao_obra_1':['id_relatorio_1',...]}...]

Essa função irá criar um dataframe com cada pessoa dos relatórios e assim retornar esse dataframe com as seguintes informações:

- numero relatorio.
- data RDO.
- Nome obra.
- Nome.
- Nome empresa.
- Não conforme?.
- Intervalo Hora.
- horario SAM.
- horario RDO.
- incosistencia Acesso.
- valor total horas trabalhadas
"""
def CriaRelatorioObra(vetorObraRelatorio):
    """
    Cria um DataFrame de relatórios de obras.

    Args:
        vetorObraRelatorio (list): lista de dicionários no formato:
            [
              {id_obra_1: [id_relatorio_1, id_relatorio_2, ...]},
              {id_obra_2: [id_relatorio_1, ...]},
              ...
              {id_obra_n: [id_relatorio_1, ...]}
            ]

    Returns:
        pd.DataFrame: com as colunas:
            - Numero Relatorio
            - Data RDO
            - Nome Obra
            - Nome Pessoa
            - Nome Empresa
            - Nome Func.
            - Nao Conforme?
            - Intervalo Hora
            - Horario SAM
            - Horario RDO
            - Incosisten. Acesso
            - Valor Horas Trabalhadas
    """
    columns = [
        'Numero Relatorio',
        'Data RDO',
        'Nome Obra',
        'Nome',
        'Nome Empresa',
        'Nao Conforme?',
        'Intervalo Hora',
        'Horario SAM',
        'Horario RDO',
        'Incosisten. Acesso',
        'Valor Horas Trabalhadas'
    ]
    df = pd.DataFrame(columns=columns)

    # vetorObraRelatorio é algo como [{id_obra1: [rel1, rel2]}, {id_obra2: [...]}]
    for elemento in vetorObraRelatorio:
        # elemento é um dicionário, pegamos a chave e o valor (lista de relatórios)
        id_obra = list(elemento.keys())[0]
        lista_relatorios = elemento[id_obra]

        for relatorio in lista_relatorios:
            # A função VisualizarRelatorio deve retornar o JSON com as pessoas:
            pessoas = VisualizarRelatorio(id_obra, relatorio).json()['maoDeObra']['personalizada']

            # Supondo que RetornaDataNumeroNomeObra retorne [data_RDO, numero, nome_obra]
            data_RDO, numero, nome_obra = RetornaDataNumeroNomeObra(id_obra, relatorio)

            # Montar uma linha do DataFrame para cada pessoa
            for pessoa in pessoas:
                row_data = [
                    numero,                          # Numero Relatorio
                    data_RDO,                        # Data RDO
                    nome_obra,                       # Nome Obra
                    pessoa.get('nome', ''),          # Nome Pessoa
                    'LMI',                           # Nome Empresa (ajuste se necessário)
                    0,                               # Nao Conforme? (ou False, se quiser boolean)
                    '',                              # Intervalo Hora (ex.: diferença de horas, se houver)
                    '',                              # Horario SAM (preencha se tiver a info)
                    pessoa.get('horaInicio', ''),    # Horario RDO (ou horaFim, conforme sua lógica)
                    '',                              # Incosisten. Acesso (preencha se necessário)
                    pessoa.get('horasTrabalhadas', 0)# Valor Horas Trabalhadas
                ]

                # Inserir a nova linha no DataFrame
                df.loc[len(df)] = row_data

    return df
#ConferenciaBases-------------------------------------------------------------------------------------------------------
import pandas as pd

def ConferenciaBases(df: pd.DataFrame, df_acesso: pd.DataFrame) -> pd.DataFrame:
    """
    Função que realiza a conferência entre as bases `df` e `df_acesso`, verificando inconsistências de acesso,
    calculando diferenças de horário e classificando registros como "Não Conforme" quando necessário.

    Parâmetros:
    - df: DataFrame principal contendo os registros de entrada e saída.
    - df_acesso: DataFrame contendo os horários de acesso dos funcionários.

    Retorno:
    - DataFrame `df` atualizado com as colunas 'Horario SAM', 'Intervalo Hora' e 'Nao Conforme?' preenchidas corretamente.
    """

    # Formatação inicial das colunas de data e horário
    # Converter 'Horario RDO' para datetime e depois para string HH:MM
    df['Horario RDO'] = pd.to_datetime(df['Horario RDO'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
    df['Data RDO'] = pd.to_datetime(df['Data RDO'], dayfirst=True, errors='coerce')
    df_acesso['1ª Acesso'] = pd.to_datetime(df_acesso['1ª Acesso'], format='%H:%M', errors='coerce')
    df_acesso['DT Acesso'] = pd.to_datetime(df_acesso['DT Acesso'], dayfirst=True, errors='coerce')

    # Inicializar colunas se não existirem
    df['Nao Conforme?'] = df.get('Nao Conforme?', 'Não').astype(str)
    df['Horario SAM'] = df.get('Horario SAM', pd.NaT)
    df['Intervalo Hora'] = df.get('Intervalo Hora', pd.NaT)

    # Marca inconsistências de acesso
    df['Incosisten. Acesso'] = df['Nome'].apply(lambda x: 'Não' if x in df_acesso['Nome'].values else 'Sim')

    # Iteração sobre o DataFrame para conferência dos horários
    for index, row in df.iterrows():
        if row['Nome'] in df_acesso['Nome'].values:  # Se o nome estiver na base de acesso
            acessos_filtrados = df_acesso[(df_acesso['Nome'] == row['Nome']) &
                                        (df_acesso['DT Acesso'] == row['Data RDO'])]

            if not acessos_filtrados.empty:
                row_acesso = acessos_filtrados.iloc[0]  # Pega o primeiro acesso encontrado

                # Converter 'Horario RDO' de volta para datetime para cálculos
                horario_rdo = pd.to_datetime(row['Horario RDO'], format='%H:%M', errors='coerce')
                horario_sam = row_acesso['1ª Acesso']

                # Verifica se os horários são válidos
                if pd.isna(horario_rdo) or pd.isna(horario_sam):
                    continue  # Pula a iteração se houver valores inválidos

                # Combinar data de 'Data RDO' com os horários para cálculo correto
                data_base = row['Data RDO']
                if pd.notna(data_base):
                    horario_rdo_completo = pd.Timestamp.combine(data_base.date(), horario_rdo.time())
                    horario_sam_completo = pd.Timestamp.combine(data_base.date(), horario_sam.time())

                    # Calcula a diferença em horas (decimal)
                    intervalo_hora = (horario_sam_completo - horario_rdo_completo).total_seconds() / 3600

                    # Converter para formato HH:MM
                    intervalo_abs = abs(intervalo_hora)  # Usa o valor absoluto
                    horas = int(intervalo_abs)
                    minutos = int((intervalo_abs - horas) * 60)
                    intervalo_formatado = f"{horas:02d}:{minutos:02d}"

                    # Atribuir valores às colunas
                    df.at[index, 'Horario SAM'] = horario_sam.strftime('%H:%M')
                    df.at[index, 'Horario RDO'] = horario_rdo.strftime('%H:%M')  # Garantir que seja apenas HH:MM
                    df.at[index, 'Intervalo Hora'] = intervalo_formatado  # Armazena como HH:MM
                    df.at[index, 'Nao Conforme?'] = 'Sim' if intervalo_abs >= 0.5 else 'Não'

    return df

#ExecutarAnalise---------------------------------------------------------------------------
data = """Nome Errado\tNome Correto
ALCILENE ALMEIDA DA VITORIA FRACALOSSI\tALCILENE ALMEIDA
ANDREA CRISTINA OLIVEIRA\tANDREA CRISTINA DE OLIVEIRA
CLEBERSON FRANCISCO FRANCA PEREIRA\tCLEBERSON FRANCISCO FRANCA
DANIEL GONCALVES DA SILVA\tDANIEL GONÇALVES DA SILVA
DIONES RODRIGO SILVA TEXEIRA\tDIONES RODRIGO SILVA TEIXEIRA
FILIPE  ALMEIDA DA VITORIA\tFILIPE ALMEIDA DA VITORIA
GUILHERME MARCHESI NOGUEIRA\tGUILHERME MARCHEZI NOGUEIRA
JACKSON CARNEIRO CORRE\tJACKSON CARNEIRO CORREA
JEFERSON BOMFIM REIS\tJEFERSON BOMFIM REIS
MAURO JORGE ALVES DE SOUZA\tMAURO JORGE ALVES
MIQUEIAS DE ALMEIDA BARCELOS\tMIQUEIAS DE ALMEIDA BAECELOS
RHUAN SANTOS OLIVEIRA\tRUHAN SANTOS OLIVEIRA
THIAGO ANSELMO  FERREIRA SIMAO\tTHIAGO ANSELMO FERREIRA SIMAO
VINICIUS PIMENTEL SCHUTLZ\tVINICIUS PIMENTEL SCHUTZ
WENYS VENANCIO MONTEIRO\tWENIS VENANCIO MONTEIRO
GERALDO CARLOS SOUZA NETO\tGERALDO CARLOS DE SOUZA NETO
MAXIMO JOSE ROSA SANT'ANA\tMAXIMO JOSE ROSA SANT ANA
CLAUDENBERG SOUZA DE OLIVEIRA\tCLAUDEMBERG SOUZA OLIVEIRA
JEFERSON BOMFIM REIS (96000534)\tJEFERSON BOMFIM REIS
"""
def VerificarHoraExcedente(hora_entrada):
  if hora_entrada is None:
      return 0

  hora = int(hora_entrada.split(":")[0])
  minuto =int( hora_entrada.split(":")[1])
  df = minuto - 14 
  if hora == 9 and df > 0:
    return df/60
  elif hora > 9:
      return abs(df)/60+ (hora - 9)
def ExecutarAnalise(df_entrada,data_inicio,data_fim):
    """
    Funcao responsável por executar a análise pegando a base de dado de entrada para validação.
    data de inicio e a data fim, gerando um dataframe final com os dados.
    """
    df_referencia = create_dataframe_from_string(data)
    df_acesso= CorrigirDados(df_entrada, df_referencia)
    
    #Id_Obras---------------------------------------------------------------------------------------
    inicio = time.time() 
    obras_id = RetornaVetorIdObras()
    fim  = time.time()
    st.write(f'Tempo para executar:RetornaVetorIdObras  {fim-inicio}')
    #Retornar todos os relatorios de um Id_Obra------------------------------------------------------
    sum = 0
    inicio = time.time()
    ids_relatorios = PegarTodosRelatoriosObras(obras_id,data_inicio,data_fim)
    fim  = time.time()
    st.write(f'Tempo para executar:PegarTodosRelatoriosObras  {fim-inicio}')
    sum+=fim-inicio
    inicio = time.time()
    df = CriaRelatorioObra(ids_relatorios)
    fim  = time.time()
    st.write(f'Tempo para executar:CriaRelatorioObra  {fim-inicio}')
    sum+=fim-inicio
    df = CorrigirDados(df,df_referencia)
    inicio = time.time()
    df_final = ConferenciaBases(df,df_acesso)
    fim  = time.time()
    st.write(f'Tempo para executar:ConferenciaBases  {fim-inicio}')
    sum+=fim-inicio
    df_final['Data RDO'] = df_final['Data RDO'].dt.date
    st.write(f'Tempo Total: {sum}')
    # Usando apply com uma função lambda para aplicar a lógica condicional
    df_final['Tempo Horas Trabalhadas Excedentes'] = df_final['Valor Horas Trabalhadas'].apply(
        lambda x: 0 if not VerificarHoraExcedente(x) else VerificarHoraExcedente(x)
    )

    return df_final
    
#Valida Datas Entrada/ Datas Planilha de Entrada--------------------------------------------------------------

def ValidaDatas(df,data_inicial,data_final):
    """
    Essa funcao recebe um dataframe que refere-se ao dataframe extraido do RDO
    e verifica se o intervalo de data fornecido pelo usuario corresponde ao que 
    esta na planilha
    args:
        df: Dataframe
        data_inicial: Data Inicial Streamlit
        data_final: Data Final Streamlit
    """
    data_minima = str(df['DT Acesso'].min()).split(' ')[0]
    data_maxima = str(df['DT Acesso'].max()).split(' ')[0]
    if data_minima == str(data_inicial) and str(data_final) == data_maxima:
        return True
    else: 
        return False
#Salvar Dataframe como Excel-----------------------------------------------------------------
def salvar_dataframe_em_excel(df: pd.DataFrame) -> io.BytesIO:
    """
    Converte um DataFrame em um buffer binário no formato Excel (.xlsx).

    Parâmetros:
    - df: DataFrame a ser convertido.

    Retorna:
    - buffer: Um objeto BytesIO contendo o arquivo Excel.

    Levanta:
    - ValueError: Se o DataFrame for inválido.
    - Exception: Se houver erro ao converter para Excel.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("O argumento 'df' deve ser um pandas DataFrame.")
    if df.empty:
        raise ValueError("O DataFrame está vazio. Não é possível gerar um arquivo Excel.")
    
    try:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)  # Volta o ponteiro para o início do buffer
        return buffer
    except Exception as e:
        raise Exception(f"Erro ao converter o DataFrame para Excel: {e}")
    
#Verificar Arquivo Excel----------------------------------------------------------------------
def verificar_arquivo_excel(caminho_arquivo: str) -> bool:
    """
    Verifica se um arquivo Excel existe e pode ser lido.

    Parâmetros:
    - caminho_arquivo (str): Caminho completo ou relativo do arquivo Excel (.xlsx ou .xls).

    Retorna:
    - bool: True se o arquivo existe e pode ser lido, False caso contrário.
    """
    try:
        # Verifica se o arquivo existe no sistema de arquivos
        if not os.path.exists(caminho_arquivo):
            return False
        
        # Tenta ler o arquivo Excel
        pd.read_excel(caminho_arquivo, engine='openpyxl')
        return True
    except FileNotFoundError:
        # Arquivo não encontrado
        return False
    except Exception as e:
        # Outros erros (permissão, arquivo corrompido, etc.)
        print(f"Erro ao tentar acessar o arquivo {caminho_arquivo}: {e}")
        return False