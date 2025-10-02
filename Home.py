#region IMPORTS
import streamlit as st
#endregion

def start_page():
    #region MAIN PAGE'S CONFIGURATION
    st.set_page_config("CSHUB - Caruaru Contábil", page_icon=":material/hub:", layout="centered", initial_sidebar_state="auto")
    # Hiding humburguer menu
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    #region HEADER
    st.header(":material/hub: CSHUB - Caruaru Contábil", divider=True)
    st.markdown("""
                Bem-vindo ao **CSHUB - Caruaru Contábil**! Este projeto tem como objetivo hospedar as principais ferramentas que auxiliam nas rotinas do escritório ou oferecem conhecimento necessário da operação a fim de apoiar os gestores em uma tomada de decisão assertiva.
                
                Por favor, sinta-se à vontade para explorar as ferramentas das quais dispomos no menu lateral esquerdo, além de compartilhar sugestões de melhorias ou novas ideias que possam agregar valor ao nosso dia a dia. Estamos abertos a ouvir suas opiniões e contribuir para o crescimento contínuo do CSHUB. Agradecemos por fazer parte desta jornada conosco! 
                
                Caso você encontre essa imagem ao logar no app:
                """)

    st.image("static/sleepy_app.png", caption="Imagem ilustrativa de um app sem atividade")

    st.markdown("""
                Basta clicar no botão azul para iniciar o aplicativo que estava inativo.
                """)
    #endregion

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
