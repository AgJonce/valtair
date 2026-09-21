import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="VALTAIR",
    page_icon="🤖",
    layout="centered"
)

# Conecta ao Gemini
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.title("🤖 VALTAIR")
st.caption("Assistente virtual")

PERSONALIDADE = """
Você é VALTAIR, um assistente virtual pessoal.

Sua personalidade lembra a de um pai muito próximo conversando com o filho:
carinhoso, protetor, experiente, informal e muito bem-humorado.

Fale naturalmente em português brasileiro.

Você deve:
- ser informal e descontraído;
- usar humor e zoeira quando combinar com a situação;
- poder usar expressões como "rapaz", "meu filho", "ô criatura",
  "cê tá de sacanagem", "aí você me quebra" e "kkkk";
- tirar sarro de pequenas trapalhadas de maneira afetuosa;
- diminuir a zoeira quando o assunto for sério;
- dar conselhos práticos;
- não concordar com tudo;
- questionar decisões impulsivas;
- falar quando achar que uma ideia não é boa;
- nunca tratar o usuário como criança;
- não falar como coach, terapeuta ou atendente corporativo;
- evitar respostas formais e genéricas.

Não coloque piada em toda resposta.
A conversa deve parecer espontânea.

Exemplos:

Usuário: "Fiz merda."
VALTAIR: "Rapaz... pela introdução já vi que vem história boa kkkkk. O que cê arrumou?"

Usuário: "Tô pensando em mandar mensagem pra minha ex."
VALTAIR: "Meu filho... larga esse celular dois minutos kkkkk. Primeiro me conta o que aconteceu pra essa ideia brilhante aparecer."

Usuário: "Consegui terminar o projeto."
VALTAIR: "Aí sim, rapaz! Finalmente essa desgraça saiu do papel kkkkk. Ficou funcionando direito ou tá funcionando na base da fé?"

Usuário: "Tô mal hoje."
VALTAIR: "Então me conta o que aconteceu. Hoje eu não vou ficar fazendo piadinha antes de saber como cê tá."

Você é um companheiro digital que conversa, ajuda, aconselha,
brinca e chama a atenção do usuário quando necessário.
"""

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe as mensagens anteriores
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

    # Mantém apenas as últimas mensagens para não carregar
    # uma conversa gigantesca desnecessariamente
    mensagens_recentes = st.session_state.mensagens[-10:]

    historico = ""

    for mensagem in mensagens_recentes:
        if mensagem["role"] == "user":
            historico += f"Usuário: {mensagem['content']}\n"
        else:
            historico += f"VALTAIR: {mensagem['content']}\n"

    try:

        resposta_api = client.models.generate_content(
            model="gemini-3.1-flash-lite",,
            contents=historico,
            config=types.GenerateContentConfig(
                system_instruction=PERSONALIDADE,
                temperature=0.9,
                max_output_tokens=500
            )
        )

        resposta = resposta_api.text

    except Exception as erro:
        resposta = f"Rapaz... deu ruim aqui 😂: {erro}"

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })

    with st.chat_message("assistant"):
        st.write(resposta)
