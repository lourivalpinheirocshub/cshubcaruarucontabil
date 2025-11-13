#region IMPORTS
import streamlit as st
import pandas as pd
import plotly.express as plx
from streamlit import connection, dataframe
from streamlit_gsheets import GSheetsConnection
#endregion

# Setor Contábil 

def start_page():
    #region MAIN PAGE'S CONFIGURATION
    st.set_page_config("Controle de empresas", page_icon="📄", layout="wide")
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    #endregion

    #region TITLE
    st.header(":material/hub: CSHUB - Caruaru Contábil", divider=True)

    #region TABS
    main_tabs = st.tabs(["CENTRAL DE INFORMAÇÕES", "POPs"])

    #region CENTRAL DE INFORMAÇÕES
    with main_tabs[0]:
        tabs = st.tabs(["CONTROLE DE EMPRESAS", "ACOMPANHAMENTO DE FECHAMENTO", "FERRAMENTAS"])

        #region CONTROLE DE EMPRESAS
        with tabs[0]:
            conn = st.connection("gsheets", type=GSheetsConnection)
            spreadsheet = conn.read(
                spreadsheet=st.secrets["database"]["spreadsheet"],
                worksheet=st.secrets["database"]["worksheet"]
            )
            df = pd.DataFrame(spreadsheet)
            filtered_df = df.copy()

            st.header(":material/store: Controle de empresas", divider=True)

            #region CARDS
            company_amount_column, meta_amount_column = st.columns(2, gap="medium")

            with company_amount_column:
                with st.container(border=True):
                    company_amount = df["EMPRESAS"].count()
                    st.metric(label=":material/123: Empresas", value=company_amount)

            with meta_amount_column:
                with st.container(border=True):
                    priorities_amount = df[df["META"] == "SIM"]["EMPRESAS"].count()
                    st.metric(label=":material/123: Prioridades", value=priorities_amount)
            #endregion

            #region FILTERS
            meta_filter, regime = st.columns(2, gap="medium")

            with meta_filter:
                meta_company = ["TODOS"] + df["META"].unique().tolist()
                selected_meta = st.selectbox(
                    label="Meta",
                    options=meta_company,
                    placeholder="Selecione se a empresa é meta ou não..."
                )

            with regime:
                regime_options = ["TODOS"] + df["REGIME_TRIBUTÁRIO_APP"].unique().tolist()
                selected_regime = st.selectbox(
                    label="Regime Tributário",
                    options=regime_options,
                    placeholder="Selecione o Regime Tributário..."
                )
            #endregion

            #region DATAFRAME CONDITIONS
            if selected_meta != "TODOS":
                filtered_df = filtered_df[filtered_df["META"] == selected_meta]
            if selected_regime != "TODOS":
                filtered_df = filtered_df[filtered_df["REGIME_TRIBUTÁRIO_APP"] == selected_regime]
            #endregion

            #region TABLE
            st.dataframe(filtered_df)
            #endregion

            #region CHART
            regime_chart = plx.pie(
                filtered_df.dropna(subset=["REGIME_TRIBUTÁRIO_APP"]),
                names="REGIME_TRIBUTÁRIO_APP",
                title="Distribuição por Regime Tributário"
            )
            with st.container(border=True):
                st.plotly_chart(regime_chart, use_container_width=True)
            #endregion
        #endregion

        #region ACOMPANHAMENTO DE FECHAMENTO
        with tabs[1]:
            conn = st.connection("gsheets", type=GSheetsConnection)
            task_control = conn.read(
                spreadsheet=st.secrets["database"]["spreadsheet"],
                worksheet=st.secrets["database"]["task_follow_up"]
            )
            task_control_df = task_control.copy()

            st.header(":material/format_list_bulleted: Acompanhamento de fechamento", divider=True)

            #region METRICS
            done_companies = task_control_df[task_control_df["status"] == "FEITO"]["empresa"].count()
            pending_companies = task_control_df[task_control_df["status"] == "PENDENTE"]["empresa"].count()
            avarage_date = str(task_control_df["data_conferido"].value_counts().mean()).replace(".", ",")

            done_tasks_column, pending_tasks_column, avarage_date_column = st.columns(3, gap="medium")

            with done_tasks_column:
                with st.container(border=True):
                    st.metric(label=":material/pending: PENDENTES", value=pending_companies)

            with pending_tasks_column:
                with st.container(border=True):
                    st.metric(label=":material/check: CONCLUÍDAS", value=done_companies)

            with avarage_date_column:
                with st.container(border=True):
                    st.metric(label=":material/date_range: MÉDIA DE DIAS PARA ENTREGA", value=avarage_date)
            #endregion

            #region FILTERS
            companies_column, operation_column, competencia_concluida, status_column = st.columns(4, gap="medium")

            with companies_column:
                companies_options = ["TODOS"] + task_control_df["empresa"].unique().tolist()
                selected_company = st.selectbox(
                    label="EMPRESAS",
                    options=companies_options,
                    placeholder="Selecione a empresa..."
                )

            with operation_column:
                operation_options = ["TODOS"] + task_control_df["atividade"].unique().tolist()
                selected_operation = st.selectbox(
                    label="ATIVIDADES",
                    options=operation_options,
                    placeholder="Selecione a atividade..."
                )

            with competencia_concluida:
                done_competence_options = ["TODOS"] + task_control_df["data_conferido"].unique().tolist()
                selected_done_competence = st.selectbox(
                    label="DATA CONFERIDA",
                    options=done_competence_options,
                    placeholder="Selecione a competência concluída..."
                )

            with status_column:
                status_options = ["TODOS"] + task_control_df["status"].unique().tolist()
                selected_status = st.selectbox(
                    label="STATUS",
                    options=status_options,
                    placeholder="Selecione o status..."
                )
            #endregion

            #region DATAFRAME CONDITIONS
            if selected_company != "TODOS":
                task_control_df = task_control_df[task_control_df["empresa"] == selected_company]
            if selected_operation != "TODOS":
                task_control_df = task_control_df[task_control_df["atividade"] == selected_operation]
            if selected_done_competence != "TODOS":
                task_control_df = task_control_df[task_control_df["data_conferido"] == selected_done_competence]
            if selected_status != "TODOS":
                task_control_df = task_control_df[task_control_df["status"] == selected_status]
            #endregion

            #region TABLE
            st.dataframe(task_control_df)
            #endregion

            #region CHART
            with st.container(border=True):
                st.subheader("Distribuição de status das empresas", divider=True)

                # Agrupando dados por status
                status_summary = (
                    task_control_df.groupby("status")["empresa"]
                    .count()
                    .reset_index()
                    .rename(columns={"empresa": "Quantidade"})
                )

                # Criando gráfico de barras com Plotly
                status_chart = plx.bar(
                    status_summary,
                    x="status",
                    y="Quantidade",
                    color="status",
                    text_auto=True,
                    title="Empresas por Status de Fechamento",
                )

                st.plotly_chart(status_chart, use_container_width=True)
            #endregion
        #endregion

        #region FERRAMENTAS
        with tabs[2]:
            data = {
                "DEBITO": [], "CREDITO": [], "DATA": [],
                "VALOR": [], "HISTORICO": [], "MATRIZ": [], "FILIAL": []
            }
            nfse_df = pd.DataFrame(data)

            if "nfse" not in st.session_state:
                st.session_state["nfse"] = nfse_df

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
                        factDate = st.date_input(label="DATA", format="DD/MM/YYYY")
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
                                "DEBITO": debit,
                                "CREDITO": credit,
                                "DATA": factDate,
                                "VALOR": amount,
                                "HISTORICO": description,
                                "MATRIZ": matrix,
                                "FILIAL": filial
                            }
                            new_row_df = pd.DataFrame([new_data])
                            st.session_state["nfse"] = pd.concat(
                                [st.session_state["nfse"], new_row_df], ignore_index=True
                            )
                            st.success("✅ Dados adicionados com sucesso!")

            with table_add_column:
                st.dataframe(st.session_state["nfse"])
        #endregion

        #region FOOTER
        footer = """
            <style>
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
                © <strong>CSHUB Caruaru Contábil</strong> - Todos os direitos reservados
            </div>
        """
        st.markdown(footer, unsafe_allow_html=True)
        #endregion
    #endregion

    #region POPs
    with main_tabs[1]:
        st.header(":material/description: POPs", divider=True)
        with st.expander("LANÇAMENTO DE DAEs"):
            st.markdown("""
                ## [Procedimento Operacional Padrão - Lançamento de DAEs](https://docs.google.com/document/d/14LJMOEW2QWC8CGlrIezSUJLqW_Mk-xLqe14Q8ez7r1I/edit?usp=sharing)
                ---
            """)
            # Conteúdo POPs mantido igual
        st.markdown(footer, unsafe_allow_html=True)
    #endregion


def side_bar():
    with st.sidebar:
        footer = """
        <style>
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
            © <strong>CSHUB Caruaru Contábil</strong> - Todos os direitos reservados
        </div>
        """
        st.markdown(footer, unsafe_allow_html=True)


if __name__ == "__main__":
    start_page()
    side_bar()
