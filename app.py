import streamlit as st

st.set_page_config(
    page_title="VALTAIR",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 VALTAIR")
st.caption("Assistente virtual")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

pergunta = st.chat_input("Fale comigo...")

if pergunta:
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.write(pergunta)

    resposta = f"Você disse: {pergunta}"

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })

    with st.chat_message("assistant"):
        st.write(resposta)
