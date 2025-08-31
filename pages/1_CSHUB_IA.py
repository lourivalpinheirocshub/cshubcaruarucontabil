#region IMPORTS
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
#endregion

def start_page():
    #region INITIALIZING MEMORY
    memory = ConversationBufferMemory()
    #endregion

    #region API KEY
    api_key = st.secrets["ai"]["OPEN_AI_KEY"]
    #enregion

    #region INITIALIZING MODEL
    chat = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, streaming=True)
    st.session_state['chat_model'] = chat
    #endregion
    
    #region PAGE'S CONFIGURATION
    st.set_page_config("CSHUB IA", ":material/robot_2:", layout="centered")
    # Hiding humburguer menu
    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.header(":material/robot_2: CSHUB IA", divider=True)
    #endregion

    #region GETTING CHAT AND MEMORY
    chat_model = st.session_state.get("chat_model")
    model_memory = st.session_state.get('memory', memory)
    #endregion

    #region CHAT HISTORY
    for messages in model_memory.buffer_as_messages:
        chat = st.chat_message(messages.type)
        chat.markdown(messages.content)
    #endregion

    #region INPUT
    user_input = st.chat_input("Pergunte à CSHUB IA...")
    if user_input:
        model_memory.chat_memory.add_user_message(user_input)

        chat = st.chat_message('human')
        chat.markdown(user_input)

        chat = st.chat_message("ai")
        answer = chat.write_stream(chat_model.stream(user_input))

        model_memory.chat_memory.add_ai_message(answer)
        st.session_state['memory'] = model_memory

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
        © <strong>CSHUB - Caruaru Contábil<strong/> - Todos os direitos reservados
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
    #endregion

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
                © <strong>CSHUB - Caruaru Contábil<strong/> - Todos os direitos reservados
            </div>
            """
        st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    start_page()
    side_bar()
