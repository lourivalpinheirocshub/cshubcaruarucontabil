#region IMPORTS
import streamlit as st
import pandas as pd
import plotly.express as plx
from streamlit import connection, dataframe
from streamlit_gsheets import GSheetsConnection
#endregion

def start_page():
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


        #region FILTERS
        meta_filter, regime = st.columns(2, gap="medium")
        with meta_filter:
            # meta_filter
            meta_company = ["TODOS"] + df["META"].unique().tolist()
            selected_meta = st.selectbox(
                label="Meta",
                options=meta_company,
                placeholder="Selecione se a empresa é meta ou não..."
            )


        with regime:
            # documentation_filter
            regime = ["TODOS"] + df["REGIME_TRIBUTÁRIO_APP"].unique().tolist()
            selected_regime = st.selectbox(
                label="Regime Tributário",
                options=regime,
                placeholder="Selecione o Regime Tributário..."
            )

        #region DATAFRAME CONDITIONS
        if selected_meta != "TODOS":
            filtered_df =  filtered_df[filtered_df["META"] == selected_meta]

        if selected_regime != "TODOS":
            filtered_df = filtered_df[filtered_df["REGIME_TRIBUTÁRIO_APP"] ==  selected_regime]


        #region TABLE
        st.dataframe(filtered_df)
        #endregion


        regime_chart = plx.pie(
            filtered_df.dropna(subset=["REGIME_TRIBUTÁRIO_APP"]),
            names="REGIME_TRIBUTÁRIO_APP",
            title="Distribuição por Regime Tributário",)
        with st.container(border=True):
            st.plotly_chart(regime_chart, use_container_width=True)

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

        form_column, table_add_column = st.columns(2, gap="medium")
        with form_column:
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

        with table_add_column:
            st.dataframe(st.session_state["nfse"])

    footer = """
        <style>
        /* Hide default Streamlit footer */
        footer {visibility: hidden;}

        .footer-custom {
            position: relative;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: #ffff;
            padding: 10px 0;
            margin-top: auto;
        }
        </style>

        <div class="footer-custom">
            © <strong>CSHUB Caruaru Contábil<strong/> - Todos os direitos reservados
        </div>
        """
    st.markdown(footer, unsafe_allow_html=True)

def side_bar():
    with st.sidebar:
        footer = """
        <style>
        /* Hide default Streamlit footer */
        footer {visibility: hidden;}

        .footer-custom {
            position: relative;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: #ffff;
            padding: 10px 0;
            margin-top: auto;
        }
        </style>

        <div class="footer-custom">
            © <strong>CSHUB Caruaru Contábil<strong/> - Todos os direitos reservados
        </div>
        """
        st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    start_page()
    side_bar()
