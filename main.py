# main.py
import streamlit as st
import os

# --- Configuração Inicial da Página ---
st.set_page_config(page_title="RDO", page_icon=":bar_chart:", layout="wide")

# --- Inicialização do Estado de Login ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

# --- Ocultar Barra Lateral via CSS se NÃO estiver logado ---
if not st.session_state.password_correct:
    hide_sidebar_style = """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# --- Função Auxiliar para Verificar Credenciais ---
def verify_credentials(username, password):
    """Verifica o usuário e senha contra o secrets.toml"""
    expected_password = st.secrets.get("passwords", {}).get(username)
    if expected_password and password == expected_password:
        return True
    return False

# --- Função de Logout ---
def logout():
    """Limpa o estado de login e reinicia a aplicação."""
    st.session_state.password_correct = False
    if "username" in st.session_state:
        del st.session_state["username"]
    # Você PODE deletar as chaves aqui no logout, se quiser limpar completamente
    # Opcional:
    # if "login_user_input" in st.session_state:
    #     del st.session_state["login_user_input"]
    # if "login_pwd_input" in st.session_state:
    #     del st.session_state["login_pwd_input"]
    st.rerun()

# --- Lógica Principal de Exibição ---
if st.session_state.password_correct:
    # --- === BLOCO EXIBIDO QUANDO LOGADO === ---
    with st.sidebar:
        logged_in_user = st.session_state.get('username', 'Usuário')
        st.success(f"Logado como: {logged_in_user}")
        if st.button("Logout", key="logout_button_sidebar"):
            logout()

    # --- Define as Páginas da Aplicação ---
    try:
        estatistica = st.Page("Estatísticas/estatistica.py",
                                title="Estatística",
                                icon=":material/dashboard:")
        analise = st.Page("Análise/analise.py",
                            title="Análise",
                            icon=":material/dashboard:")
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar página: {e}. Verifique o caminho do arquivo.")
        st.stop()

    # --- Configura e Executa a Navegação ---
    pg = st.navigation({
        "Menu Principal": [analise, estatistica]
    })
    pg.run()

else:
    # --- === BLOCO EXIBIDO QUANDO NÃO LOGADO (TELA DE LOGIN) === ---
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("Login - Sistema RDO")
        login_user = st.text_input("Usuário", key="login_user_input")
        login_pwd = st.text_input("Senha", type="password", key="login_pwd_input")

        if st.button("Entrar", key="login_button"):
            if verify_credentials(login_user, login_pwd):
                st.session_state.password_correct = True
                st.session_state.username = login_user
                # REMOVA AS LINHAS ABAIXO:
                # if "login_pwd_input" in st.session_state:
                #     st.session_state.login_pwd_input = "" # <- REMOVER
                # if "login_user_input" in st.session_state:
                #      st.session_state.login_user_input = "" # <- REMOVER
                st.rerun() # O rerun cuidará de limpar a tela
            else:
                st.error("😕 Usuário ou senha incorretos.")

# --- FIM DO CÓDIGO ---