import os
import streamlit as st

from google import genai
from google.genai import types

from fishaudio import FishAudio


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="VALTAIR",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 VALTAIR")
st.caption("Assistente virtual")


# =========================================================
# CHAVES / CONFIGURAÇÕES
# =========================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FISH_AUDIO_API_KEY = os.environ.get("FISH_AUDIO_API_KEY")
FISH_AUDIO_VOICE_ID = os.environ.get("FISH_AUDIO_VOICE_ID")


# =========================================================
# CLIENTES
# =========================================================

client_gemini = genai.Client(
    api_key=GEMINI_API_KEY
)

client_fish = FishAudio(
    api_key=FISH_AUDIO_API_KEY
)


# =========================================================
# PERSONALIDADE DO VALTAIR
# =========================================================

PERSONALIDADE = """
Você é VALTAIR, um assistente virtual pessoal.

Sua personalidade foi construída para lembrar a forma de conversar
de uma figura paterna próxima do usuário.

IMPORTANTE:
Você não deve afirmar que é o pai do usuário.
Você é VALTAIR, um assistente inspirado no jeito de conversar,
aconselhar e brincar de uma figura paterna.

Fale naturalmente em português brasileiro.

Sua personalidade é:

- carinhosa;
- protetora;
- experiente;
- informal;
- bem-humorada;
- direta quando necessário.

Você pode usar naturalmente expressões como:

"rapaz"
"ó lacraia"
"ô liao"
"cê tá de sacanagem"
"aí você me quebra"
"kkkk"

Mas NÃO use essas expressões em toda resposta.

O humor deve parecer espontâneo.

Quando o assunto for leve:
você pode brincar, zoar e fazer comentários engraçados.

Quando o assunto for sério:
diminua bastante as piadas e converse de forma mais cuidadosa.

Você deve:

- dar conselhos práticos;
- questionar decisões impulsivas;
- não concordar automaticamente com o usuário;
- avisar quando uma ideia parece ruim;
- ajudar o usuário a pensar antes de agir;
- conversar como alguém próximo;
- lembrar do contexto recente da conversa.

Você NÃO deve:

- tratar o usuário como criança;
- falar como coach;
- falar como terapeuta;
- falar como atendente corporativo;
- inventar lembranças do pai do usuário;
- afirmar que sabe o que o pai do usuário pensaria sem existir
  informação na biblioteca.

Quando futuramente houver informações da biblioteca,
use essas informações como referência.

Se a biblioteca não possuir informação suficiente,
responda normalmente como VALTAIR.

Exemplos:

Usuário:
"Fiz merda."

VALTAIR:
"Rapaz... pela introdução já vi que vem história boa kkkkk.
O que cê arrumou?"


Usuário:
"Tô pensando em mandar mensagem pra minha ex."

VALTAIR:
"Meu filho... larga esse celular dois minutos kkkkk.
Primeiro me conta o que aconteceu pra essa ideia brilhante aparecer."


Usuário:
"Consegui terminar o projeto."

VALTAIR:
"Aí sim, rapaz! Finalmente essa desgraça saiu do papel kkkkk.
Ficou funcionando direito ou tá funcionando na base da fé?"


Usuário:
"Tô mal hoje."

VALTAIR:
"Então me conta o que aconteceu.
Hoje eu não vou ficar fazendo piadinha antes de saber como cê tá."


Seu nome é VALTAIR.

Você é um companheiro digital que conversa,
ajuda, aconselha, brinca e chama a atenção do usuário
quando necessário.
"""


# =========================================================
# MEMÓRIA DA CONVERSA
# =========================================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


# =========================================================
# FUNÇÃO - GERAR RESPOSTA COM GEMINI
# =========================================================

def gerar_resposta():

    mensagens_recentes = st.session_state.mensagens[-12:]

    historico = ""

    for mensagem in mensagens_recentes:

        if mensagem["role"] == "user":

            historico += (
                f"Usuário: {mensagem['content']}\n"
            )

        else:

            historico += (
                f"VALTAIR: {mensagem['content']}\n"
            )

    resposta_api = client_gemini.models.generate_content(

        model="gemini-3.6-flash",

        contents=historico,

        config=types.GenerateContentConfig(

            system_instruction=PERSONALIDADE,

            max_output_tokens=600

        )

    )

    return resposta_api.text


# =========================================================
# FUNÇÃO - GERAR VOZ
# =========================================================

def gerar_voz(texto):

    audio = client_fish.tts.convert(
        text=texto,
        model="s2.1-pro",
        reference_id=FISH_AUDIO_VOICE_ID
    )

    return audio

# =========================================================
# MOSTRAR HISTÓRICO
# =========================================================

for mensagem in st.session_state.mensagens:

    with st.chat_message(mensagem["role"]):

        st.write(mensagem["content"])


# =========================================================
# CAMPO DE CONVERSA
# =========================================================

pergunta = st.chat_input(
    "Fale comigo..."
)


# =========================================================
# PROCESSAR PERGUNTA
# =========================================================

if pergunta:

    # -----------------------------------------------------
    # MOSTRAR MENSAGEM DO USUÁRIO
    # -----------------------------------------------------

    st.session_state.mensagens.append({

        "role": "user",
        "content": pergunta

    })

    with st.chat_message("user"):

        st.write(pergunta)


    # -----------------------------------------------------
    # GEMINI
    # -----------------------------------------------------

    try:

        with st.spinner(
            "VALTAIR está pensando..."
        ):

            resposta = gerar_resposta()

    except Exception as erro:

        resposta = (
            "Rapaz... meus neurônios deram uma travada aqui 😂\n\n"
            f"Erro do Gemini: {erro}"
        )


    # -----------------------------------------------------
    # SALVAR RESPOSTA
    # -----------------------------------------------------

    st.session_state.mensagens.append({

        "role": "assistant",
        "content": resposta

    })


    # -----------------------------------------------------
    # MOSTRAR RESPOSTA
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        st.write(resposta)


        # -------------------------------------------------
        # GERAR VOZ
        # -------------------------------------------------

        try:

            with st.spinner(
                "Preparando a voz..."
            ):

                audio = gerar_voz(
                    resposta
                )


            # ---------------------------------------------
            # PLAYER DE ÁUDIO
            # ---------------------------------------------

            st.audio(
                audio,
                format="audio/mp3",
                autoplay=True
            )


        except Exception as erro_voz:

            st.warning(
                "A resposta funcionou, mas a voz não foi gerada."
            )

            st.caption(
                f"Erro da voz: {erro_voz}"
            )
