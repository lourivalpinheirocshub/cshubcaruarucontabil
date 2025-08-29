#region IMPORTS
import streamlit as st
import pandas as pd
import plotly.express as plx
from streamlit import connection, dataframe
from streamlit_gsheets import GSheetsConnection
#endregion


#region MAIN PAGE'S CONFIGURATION
st.set_page_config("Controle de empresas", page_icon="📄", layout="wide", initial_sidebar_state="auto")
# Hiding humburguer menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#endregion

#region CONNECTING TO DATABASE
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = conn.read(
    spreadsheet=st.secrets["database"]["spreadsheet"],
    worksheet=st.secrets["database"]["worksheet"]
)
# #endregion

# #region DATAFRAME
df = pd.DataFrame(spreadsheet)
#endregion

#region FILTERED DATAFRAME
filtered_df = df.copy()

#region HEADER
st.header("📄 Controle de empresas", divider=True)
#endregion


#region CARDS
company_amount_column, meta_amount_column, sends_docs, doesnt_docs = st.columns(4, gap="medium")
fiscal, folha, sem_parametro = st.columns(3, gap="medium")

# Amount of companies
with company_amount_column:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        companies_amount_dataframe = pd.DataFrame(companies_amount_spreadsheet)

        company_amount = companies_amount_dataframe["EMPRESAS"].count()
        st.metric(
            label=":material/123: Empresas",
            value=company_amount
        )

# Priorities of companies
with meta_amount_column:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        priorities = pd.DataFrame(companies_amount_spreadsheet)

        priorities_amount = priorities[priorities["META"] == "SIM"]["EMPRESAS"].count()
        st.metric(
            label=":material/123: Prioridades",
            value=priorities_amount
        )

with sends_docs:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        sends_docs = pd.DataFrame(companies_amount_spreadsheet)

        sends_docs_amount = sends_docs[sends_docs["DOCUMENTAÇÃO"] == "SIM"]["EMPRESAS"].count()
        st.metric(
            label=":material/123: Envia documentação",
            value=sends_docs_amount
        )

with doesnt_docs:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        not_sends_docs = pd.DataFrame(companies_amount_spreadsheet)

        not_sends_docs_amount = not_sends_docs[not_sends_docs["DOCUMENTAÇÃO"] == "NÃO"]["EMPRESAS"].count()
        st.metric(
            label=":material/123: Não envia documentação",
            value=not_sends_docs_amount
        )

with fiscal:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        fiscal = pd.DataFrame(companies_amount_spreadsheet)

        fiscal_amount = not_sends_docs[not_sends_docs["MOVIMENTO_FISCAL"] == "SIM"]["EMPRESAS"].count()
        st.metric(
            label=":material/123: Movimento Fiscal",
            value=fiscal_amount
        )

with folha:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        folha = pd.DataFrame(companies_amount_spreadsheet)

        folha_amount = folha[folha["FOLHA_PAGAMENTO"] == "SIM"]["EMPRESAS"].count()
        st.metric(
            label=":material/123: Movimento Folha",
            value=folha_amount
        )

with sem_parametro:
    with st.container(border=True):
        conn = st.connection("gsheets", type=GSheetsConnection)
        companies_amount_spreadsheet = conn.read(
            spreadsheet=st.secrets["database"]["spreadsheet"],
            worksheet=st.secrets["database"]["worksheet"]
        )
        sem_parametro = pd.DataFrame(companies_amount_spreadsheet)

        sem_parametro_fiscal = sem_parametro[sem_parametro["MOVIMENTO_FISCAL"] == "SEM PARAMETRO"]["EMPRESAS"].count()
        sem_parametro_folha = sem_parametro[sem_parametro["FOLHA_PAGAMENTO"] == "SEM PARAMETRO"]["EMPRESAS"].count()
        sem_parametro_amount = sem_parametro_fiscal + sem_parametro_folha
        st.metric(
            label=":material/123: Sem Parâmetro",
            value=sem_parametro_amount
        )

#region FILTERS
meta_filter, documentation_filter = st.columns(2, gap="medium")
with meta_filter:
    # meta_filter
    meta_company = ["TODOS"] + df["META"].unique().tolist()
    selected_meta = st.selectbox(
        label="Meta",
        options=meta_company,
        placeholder="Selecione se a empresa é meta ou não..."
    )

with documentation_filter:
    # documentation_filter
    meta_documentation = ["TODOS"] + df["DOCUMENTAÇÃO"].unique().tolist()
    selected_documentation = st.selectbox(
        label="Envia Documentação",
        options=meta_documentation,
        placeholder="Selecione se a empresa enviou a documentação..."
    )


#region DATAFRAME CONDITIONS
if selected_meta != "TODOS":
    filtered_df =  filtered_df[filtered_df["META"] == selected_meta]

if selected_documentation != "TODOS":
    filtered_df = filtered_df[filtered_df["DOCUMENTAÇÃO"] ==  selected_documentation]

#endregion

planilha, charts = st.columns(2, gap="medium")
with planilha:
    #region TABLE
    st.dataframe(filtered_df)
    #endregion

with charts:
    regiome_chart = plx.pie(
        filtered_df,
        names="REGIME_TRIBUTÁRIO_APP",
        title="Regime Tributário",)
    with st.container(border=True):
        st.plotly_chart(regiome_chart, use_container_width=True)
