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

#region TABS
tabs = st.tabs(["CONTROLE DE EMPRESAS", "CONTROLE DE DEMANDAS", "FERRAMENTAS"])
with tabs[0]:
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
    st.header(":material/store: Controle de empresas", divider=True)
    #endregion


    #region CARDS
    company_amount_column, meta_amount_column = st.columns(2, gap="medium")
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
    with company_amount_column:
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

    with meta_amount_column:
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

    with meta_amount_column:
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

    with company_amount_column:
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

    with meta_amount_column:
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
    meta_filter, documentation_filter, parameters_filter, folha_parameters = st.columns(4, gap="medium")
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

    with parameters_filter:
        # documentation_filter
        fiscal_documentation = ["TODOS"] + df["MOVIMENTO_FISCAL"].unique().tolist()
        selected_fiscal = st.selectbox(
            label="Módulo Fiscal",
            options=fiscal_documentation,
            placeholder="Selecione a situação do módulo Fiscal..."
        )

    with folha_parameters:
        # documentation_filter
        folha_documentation = ["TODOS"] + df["FOLHA_PAGAMENTO"].unique().tolist()
        select_folha = st.selectbox(
            label="Módulo Folha",
            options=folha_documentation,
            placeholder="Selecione a situação do módulo Folha..."
        )


    #region DATAFRAME CONDITIONS
    if selected_meta != "TODOS":
        filtered_df =  filtered_df[filtered_df["META"] == selected_meta]

    if selected_documentation != "TODOS":
        filtered_df = filtered_df[filtered_df["DOCUMENTAÇÃO"] ==  selected_documentation]

    if selected_fiscal != "TODOS":
        filtered_df = filtered_df[filtered_df["MOVIMENTO_FISCAL"] ==  selected_fiscal]

    if select_folha != "TODOS":
        filtered_df = filtered_df[filtered_df["FOLHA_PAGAMENTO"] ==  select_folha]
    #endregion

    #region TABLE
    st.dataframe(filtered_df)
    #endregion


    regiome_chart = plx.pie(
        filtered_df.dropna(subset=["REGIME_TRIBUTÁRIO_APP"]),
        names="REGIME_TRIBUTÁRIO_APP",
        title="Regime Tributário",)
    with st.container(border=True):
        st.plotly_chart(regiome_chart, use_container_width=True)

with tabs[1]:
    #region CONNECTION
    conn = st.connection("gsheets", type=GSheetsConnection)
    task_control = conn.read(
        spreadsheet=st.secrets["database"]["spreadsheet"],
        worksheet=st.secrets["database"]["task_control"]
    )
    task_control_df = pd.DataFrame(task_control).dropna()
    #endregion
    
    #region PAGE
    st.header(":material/format_list_bulleted: Controle de demandas", divider=True)
    
    #region METRICS
    done_tasks = task_control_df[task_control_df["status"] == "CONCLUÍDO"]["demanda"].count()
    pending_tasks = task_control_df[task_control_df["status"] == "PENDENTE"]["demanda"].count()
    avarage_date = str(task_control_df["data_entrega"].value_counts().mean()).replace(".", ",")
    
    done_tasks_column, pending_tasks_column, avarage_date_column = st.columns(3, gap="medium")
    with pending_tasks_column:
        with st.container(border=True):
            st.metric(
                    label=":material/check: CONCLUÍDAS",
                    value=done_tasks
                )
            
    with done_tasks_column:
        with st.container(border=True):
            st.metric(
                    label=":material/pending: PENDENTES",
                    value=pending_tasks
                )
            
    with avarage_date_column:
        with st.container(border=True):
            st.metric(
                    label=":material/date_range: MÉDIA DE DIAS PARA ENTREGA ",
                    value=avarage_date
                )
    #enregion
    
    submit_date_column, responsable_column, status_column, type_column = st.columns(4, gap="medium")
    with submit_date_column:
        # documentation_filter
        date_options = ["TODOS"] + task_control_df["data_entrega"].unique().tolist()
        selected_date = st.selectbox(
            label="Data de entrga",
            options=date_options,
            placeholder="Selecione a data de entrega..."
        )
        
    with responsable_column:
        # documentation_filter
        responsable_options = ["TODOS"] + task_control_df["responsavel"].unique().tolist()
        selected_responsable = st.selectbox(
            label="Responsável",
            options=responsable_options,
            placeholder="Selecione o responsável pela demanda..."
        )
    
    with status_column:
        # documentation_filter
        status_options = ["TODOS"] + task_control_df["status"].unique().tolist()
        selected_status = st.selectbox(
            label="Status",
            options=status_options,
            placeholder="Selecione o status da demanda..."
        )
        
    with type_column:
    # documentation_filter
        type_options = ["TODOS"] + task_control_df["tipo"].unique().tolist()
        selected_type = st.selectbox(
            label="Tipo",
            options=type_options,
            placeholder="Selecione o status da demanda..."
        )
        
    #region DATAFRAME CONDITIONS
    if selected_date != "TODOS":
        task_control_df =  task_control_df[task_control_df["data_entrega"] == selected_date]

    if selected_responsable != "TODOS":
        task_control_df = task_control_df[task_control_df["responsavel"] ==  selected_responsable]

    if selected_status != "TODOS":
        task_control_df = task_control_df[task_control_df["status"] ==  selected_status]

    if selected_type != "TODOS":
        task_control_df = task_control_df[task_control_df["tipo"] ==  selected_type]
    
    #region DATAFRAME
    st.dataframe(task_control_df)
    #endregion
    
    pie_column, bar_column = st.columns(2, gap="medium")
    with pie_column:
        #region CHARTS
        status_chart = plx.pie(
            task_control_df.dropna(subset=["status"]),
            names="status",
            title="Status das demandas",)
        with st.container(border=True):
            st.plotly_chart(status_chart, use_container_width=True)
    
    with bar_column:
        # Agrupando por responsável e status e contando as demandas
        responsable_status_df = task_control_df.groupby(['responsavel', 'status'])['demanda'].count().reset_index()

        # Criando o gráfico de barras
        responsable_chart = plx.bar(
            responsable_status_df,
            x="responsavel",
            y="demanda",
            color="status",
            barmode="stack",  # Empilhar as barras para cada responsável
            labels={'responsavel': 'Responsável', 'demanda': 'Quantidade de Demandas'},
            title="Demandas por Responsável",
        )

        # Exibindo o gráfico no Streamlit
        with st.container(border=True):
            st.plotly_chart(responsable_chart, use_container_width=True)

with tabs[2]:
    data = {
        "DEBITO": [],
        "CREDITO": [],
        "DATA": [],
        "VALOR": [],
        "HISTORICO": [],
        "MATRIZ": [],
        "FILIAL": []
    }
    nfse_df = pd.DataFrame(data)

    if 'nfse' not in st.session_state:
            st.session_state['nfse'] = nfse_df
    
    st.header(":material/note: NFSe", divider=True)

    with st.form("nfseData", enter_to_submit=False, clear_on_submit=True):
        debitColumn, creditColumn = st.columns(2, gap="small")
        with debitColumn:
            debit = st.text_input(label="DÉBITO")

        with creditColumn:
            credit = st.text_input(label="CRÉDITO")

        dateColumn, amountColumn = st.columns(2, gap="small")
        with dateColumn:
            factDate = st.date_input(label='DATA', format="DD/MM/YYYY")

        with amountColumn:
            amount = st.number_input(label="VALOR")

        description = st.text_area(label="HISTÓRICO", value="Vlr. da Aquisicao de Serviços Conf. NF")

        matrixColumn, filialColumn = st.columns(2, gap="small")
        with matrixColumn:
            matrix = st.text_input(label="MATRIZ")

        with filialColumn:
            filial = st.text_input(label="FILIAL")

        submit = st.form_submit_button(label="ENVIAR")

        if submit:
            if not all([debit, credit, factDate, amount, description, matrix, filial]):
                st.error("❌ Preencha todos os campos!")
            else:
                new_data = {
                    'DEBITO': debit,
                    'CREDITO': credit,
                    'DATA': factDate,
                    'VALOR': amount,
                    'HISTORICO': description,
                    'MATRIZ': matrix,
                    'FILIAL': filial
                }
                new_row_df = pd.DataFrame([new_data])
                st.session_state['nfse'] = pd.concat([st.session_state['nfse'], new_row_df], ignore_index=True)
                st.success("✅ Dados adicionados com sucesso!")

    st.dataframe(st.session_state["nfse"])
