import os
import requests
import streamlit as st

from google import genai
from google.genai import types

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="VALTAIR",
    page_icon="🤖",
    layout="centered"
)


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
# FUNÇÃO - VISUAL FUTURISTA
# =========================================================

def configurar_visual():

    st.markdown("""
    <style>

    /* FUNDO */
    .stApp {
        background:
            radial-gradient(
                circle at center,
                #061827 0%,
                #020910 45%,
                #000204 100%
            );
        color: #d8f8ff;
    }


    /* GRADE TECNOLÓGICA */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;

        background-image:
            linear-gradient(
                rgba(0, 190, 255, 0.035) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(0, 190, 255, 0.035) 1px,
                transparent 1px
            );

        background-size: 40px 40px;

        pointer-events: none;
    }


    /* LARGURA DA TELA */
    .block-container {
        max-width: 1200px;
        padding-top: 15px;
        padding-bottom: 120px;
    }


    /* TÍTULO */
    .valtair-title {
        text-align: center;

        font-size: 34px;
        font-weight: 300;

        letter-spacing: 14px;

        color: #c2f7ff;

        text-shadow:
            0 0 8px #00bfff,
            0 0 25px rgba(0,191,255,.5);

        margin-top: 5px;
    }


    .valtair-subtitle {
        text-align: center;

        color: #248db5;

        font-size: 9px;

        letter-spacing: 6px;

        margin-top: 5px;
    }


    /* HUD */
    .hud {
        position: relative;

        height: 390px;

        margin-top: 15px;
        margin-bottom: 20px;

        border-top:
            1px solid rgba(0,190,255,.25);

        border-bottom:
            1px solid rgba(0,190,255,.15);

        overflow: hidden;
    }


    /* LINHA SUPERIOR */
    .hud-line {
        position: absolute;

        top: 25px;
        left: 5%;

        width: 90%;
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #00bfff,
                transparent
            );

        box-shadow:
            0 0 8px #00bfff;
    }


    /* CÍRCULO EXTERNO */
    .hud-circle-1 {
        position: absolute;

        left: 50%;
        top: 50%;

        width: 270px;
        height: 270px;

        border-radius: 50%;

        border:
            2px solid rgba(0,190,255,.35);

        box-shadow:
            0 0 30px rgba(0,190,255,.15);

        animation:
            rotateHUD 20s linear infinite;
    }


    .hud-circle-1::before {
        content: "";

        position: absolute;

        inset: 18px;

        border-radius: 50%;

        border:
            8px dashed rgba(0,190,255,.40);

        animation:
            rotateInside 12s linear infinite;
    }


    /* CÍRCULO MÉDIO */
    .hud-circle-2 {
        position: absolute;

        left: 50%;
        top: 50%;

        width: 195px;
        height: 195px;

        border-radius: 50%;

        border:
            3px dotted rgba(55,210,255,.70);

        box-shadow:
            inset 0 0 30px rgba(0,190,255,.12),
            0 0 15px rgba(0,190,255,.15);

        animation:
            rotateHUDReverse 9s linear infinite;
    }


    /* CÍRCULO INTERNO */
    .hud-circle-3 {
        position: absolute;

        left: 50%;
        top: 50%;

        width: 125px;
        height: 125px;

        border-radius: 50%;

        border:
            5px dashed rgba(0,220,255,.60);

        animation:
            rotateHUD 6s linear infinite;
    }


    /* NÚCLEO */
    .hud-core {
        position: absolute;

        left: 50%;
        top: 50%;

        width: 55px;
        height: 55px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                #ffffff 0%,
                #9bf5ff 5%,
                #00d9ff 18%,
                #007da8 40%,
                rgba(0,80,120,.2) 65%,
                transparent 75%
            );

        box-shadow:
            0 0 10px #00d9ff,
            0 0 30px #00bfff,
            0 0 60px rgba(0,190,255,.7),
            0 0 100px rgba(0,190,255,.25);

        animation:
            pulseCore 2s ease-in-out infinite;
    }


    /* PAINEL ESQUERDO */
    .left-panel {
        position: absolute;

        left: 25px;
        top: 90px;

        width: 220px;

        color: #28bde9;

        font-family: monospace;
        font-size: 10px;

        line-height: 1.9;

        opacity: .75;

        border-left:
            2px solid rgba(0,190,255,.5);

        padding-left: 15px;
    }


    /* PAINEL DIREITO */
    .right-panel {
        position: absolute;

        right: 25px;
        top: 90px;

        width: 220px;

        text-align: right;

        color: #28bde9;

        font-family: monospace;
        font-size: 10px;

        line-height: 1.9;

        opacity: .75;

        border-right:
            2px solid rgba(0,190,255,.5);

        padding-right: 15px;
    }


    /* STATUS */
    .core-status {
        position: absolute;

        left: 50%;
        bottom: 20px;

        transform: translateX(-50%);

        font-family: monospace;

        font-size: 9px;

        letter-spacing: 4px;

        color: #00d9ff;

        text-shadow:
            0 0 10px #00bfff;
    }


    /* ANIMAÇÕES */
    @keyframes rotateHUD {

        from {
            transform:
                translate(-50%, -50%)
                rotate(0deg);
        }

        to {
            transform:
                translate(-50%, -50%)
                rotate(360deg);
        }
    }


    @keyframes rotateHUDReverse {

        from {
            transform:
                translate(-50%, -50%)
                rotate(360deg);
        }

        to {
            transform:
                translate(-50%, -50%)
                rotate(0deg);
        }
    }


    @keyframes rotateInside {

        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(-360deg);
        }
    }


    @keyframes pulseCore {

        0%, 100% {
            transform:
                translate(-50%, -50%)
                scale(.90);

            opacity: .75;
        }

        50% {
            transform:
                translate(-50%, -50%)
                scale(1.12);

            opacity: 1;
        }
    }


    /* CHAT */
    [data-testid="stChatMessage"] {
        background:
            linear-gradient(
                90deg,
                rgba(0,90,130,.10),
                rgba(0,20,35,.60)
            );

        border:
            1px solid rgba(0,190,255,.20);

        border-left:
            2px solid #009dcc;

        border-radius: 4px;

        backdrop-filter: blur(8px);
    }


    /* INPUT */
    [data-testid="stChatInput"] {
        background:
            rgba(0,10,18,.96);

        border:
            1px solid rgba(0,190,255,.5);

        border-radius: 4px;

        box-shadow:
            0 0 20px rgba(0,190,255,.12);
    }


    /* ESCONDER STREAMLIT */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* CELULAR */
    @media(max-width: 700px) {

        .hud {
            height: 300px;
        }

        .hud-circle-1 {
            width: 200px;
            height: 200px;
        }

        .hud-circle-2 {
            width: 145px;
            height: 145px;
        }

        .hud-circle-3 {
            width: 90px;
            height: 90px;
        }

        .left-panel,
        .right-panel {
            display: none;
        }

        .valtair-title {
            font-size: 24px;
            letter-spacing: 8px;
        }
    }

    </style>


    <div class="valtair-title">
        VALTAIR
    </div>

    <div class="valtair-subtitle">
        VIRTUAL ARTIFICIAL INTELLIGENCE SYSTEM
    </div>


    <div class="hud">

        <div class="hud-line"></div>


        <div class="left-panel">

            SYSTEM // VALTAIR<br>
            CORE STATUS: ONLINE<br>
            NEURAL LINK: ACTIVE<br>
            VOICE ENGINE: READY<br>
            MEMORY: STANDBY<br>
            NETWORK: CONNECTED

        </div>


        <div class="right-panel">

            ARTIFICIAL INTELLIGENCE<br>
            GEMINI ENGINE<br>
            VOICE SYNTHESIS<br>
            SECURE CHANNEL<br>
            CORE SYSTEM 01<br>
            STATUS // ACTIVE

        </div>


        <div class="hud-circle-1"></div>

        <div class="hud-circle-2"></div>

        <div class="hud-circle-3"></div>

        <div class="hud-core"></div>


        <div class="core-status">
            ● VALTAIR ONLINE
        </div>

    </div>

    """, unsafe_allow_html=True)


# =========================================================
# ATIVAR VISUAL
# =========================================================

configurar_visual()


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

    import requests

    url = "https://api.fish.audio/v1/tts"

    headers = {
        "Authorization": f"Bearer {FISH_AUDIO_API_KEY}",
        "Content-Type": "application/json",
        "model": "s2.1-pro-free"
    }

    dados = {
        "text": texto,
        "reference_id": FISH_AUDIO_VOICE_ID,
        "format": "mp3"
    }

    resposta = requests.post(
        url,
        headers=headers,
        json=dados,
        timeout=120
    )

    if resposta.status_code != 200:
        raise Exception(
            f"Fish Audio {resposta.status_code}: {resposta.text}"
        )

    return resposta.content

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
