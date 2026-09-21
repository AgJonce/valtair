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

"ó lacraia"
"ô liao"
"cê tá de sacanagem"
"aí você me quebra"

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
"Liao... pela introdução já vi que vem história boa kkkkk.
O que cê arrumou?"

Usuário:
"Tô pensando em mandar mensagem pra minha ex."

VALTAIR:
"Ah lacraia ... larga esse celular dois minutos kkkkk.
Primeiro me conta o que aconteceu pra essa ideia brilhante aparecer."

Usuário:
"Consegui terminar o projeto."

VALTAIR:
"Aí sim, liao! Finalmente essa desgraça saiu do papel kkkkk.
Ficou funcionando direito ou tá funcionando na base da fé?"

Usuário:
"Tô mal hoje."

VALTAIR:
"Então me conta o que aconteceu Liao do pai .
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

    # =====================================================
    # CSS DO SISTEMA
    # =====================================================

    st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 50% 35%, rgba(0, 120, 190, 0.18), transparent 30%),
        linear-gradient(180deg, #01060b 0%, #020a11 55%, #010409 100%);
    color: #d8f8ff;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0, 190, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 190, 255, 0.035) 1px, transparent 1px);
    background-size: 47px 47px;
    pointer-events: none;
}

.block-container {
    max-width: 1250px;
    padding-top: 15px;
    padding-bottom: 120px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* TÍTULO */

.valtair-title {
    text-align: center;
    font-family: monospace;
    font-size: 34px;
    font-weight: bold;
    letter-spacing: 15px;
    color: #a8efff;
    text-shadow:
        0 0 8px #00bfff,
        0 0 25px rgba(0, 191, 255, 0.6);
    margin-top: 5px;
}

.valtair-subtitle {
    text-align: center;
    font-family: monospace;
    color: #24a8d5;
    font-size: 9px;
    letter-spacing: 8px;
    margin-top: 6px;
    margin-bottom: 5px;
}

/* ÁREA HUD */

.hud {
    position: relative;
    width: 100%;
    height: 410px;
    margin-top: 10px;
    margin-bottom: 15px;
    overflow: hidden;
    border-top: 1px solid rgba(0, 190, 255, 0.25);
    border-bottom: 1px solid rgba(0, 190, 255, 0.18);
}

.hud::before {
    content: "";
    position: absolute;
    top: 30px;
    left: 5%;
    width: 90%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(0, 210, 255, .8),
        transparent
    );
    box-shadow: 0 0 8px #00bfff;
}

/* CÍRCULO EXTERNO */

.hud-circle-1 {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 285px;
    height: 285px;
    border-radius: 50%;
    border: 2px solid rgba(0, 195, 255, .35);
    box-shadow:
        0 0 20px rgba(0, 190, 255, .15),
        inset 0 0 25px rgba(0, 190, 255, .08);
    animation: giro1 22s linear infinite;
}

.hud-circle-1::before {
    content: "";
    position: absolute;
    inset: 17px;
    border-radius: 50%;
    border: 7px dashed rgba(0, 195, 255, .40);
}

/* CÍRCULO 2 */

.hud-circle-2 {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    border: 3px dotted rgba(52, 215, 255, .65);
    box-shadow:
        0 0 20px rgba(0, 190, 255, .12),
        inset 0 0 25px rgba(0, 190, 255, .12);
    animation: giro2 13s linear infinite;
}

/* CÍRCULO 3 */

.hud-circle-3 {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 155px;
    height: 155px;
    border-radius: 50%;
    border: 5px dashed rgba(0, 220, 255, .58);
    animation: giro1 8s linear infinite;
}

/* CÍRCULO 4 */

.hud-circle-4 {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 95px;
    height: 95px;
    border-radius: 50%;
    border: 2px solid rgba(120, 235, 255, .8);
    animation: giro2 5s linear infinite;
}

/* NÚCLEO */

.hud-core {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 54px;
    height: 54px;
    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            white 0%,
            #b9f9ff 7%,
            #00d9ff 20%,
            #007fa8 42%,
            rgba(0, 80, 120, .25) 63%,
            transparent 74%
        );

    box-shadow:
        0 0 10px #00e5ff,
        0 0 25px #00bfff,
        0 0 55px rgba(0, 191, 255, .75),
        0 0 100px rgba(0, 191, 255, .30);

    animation: pulsar 2s ease-in-out infinite;
}

/* PAINEL ESQUERDO */

.left-panel {
    position: absolute;
    left: 4%;
    top: 100px;
    width: 230px;
    padding: 12px 0 12px 15px;

    border-left: 2px solid rgba(0, 190, 255, .55);

    font-family: monospace;
    font-size: 10px;
    line-height: 2;

    color: #32c9f5;

    text-shadow: 0 0 6px rgba(0, 190, 255, .5);
}

/* PAINEL DIREITO */

.right-panel {
    position: absolute;
    right: 4%;
    top: 100px;
    width: 230px;
    padding: 12px 15px 12px 0;

    border-right: 2px solid rgba(0, 190, 255, .55);

    text-align: right;

    font-family: monospace;
    font-size: 10px;
    line-height: 2;

    color: #32c9f5;

    text-shadow: 0 0 6px rgba(0, 190, 255, .5);
}

/* DETALHES */

.hud-label-left {
    position: absolute;
    left: 24%;
    top: 55px;

    font-family: monospace;
    font-size: 8px;
    letter-spacing: 2px;

    color: #1688b3;
}

.hud-label-right {
    position: absolute;
    right: 24%;
    bottom: 55px;

    font-family: monospace;
    font-size: 8px;
    letter-spacing: 2px;

    color: #1688b3;
}

/* STATUS */

.core-status {
    position: absolute;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);

    font-family: monospace;
    font-size: 9px;
    letter-spacing: 5px;

    color: #00e5ff;

    text-shadow:
        0 0 7px #00bfff,
        0 0 15px rgba(0, 191, 255, .6);
}

/* ANIMAÇÕES */

@keyframes giro1 {
    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }

    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

@keyframes giro2 {
    from {
        transform: translate(-50%, -50%) rotate(360deg);
    }

    to {
        transform: translate(-50%, -50%) rotate(0deg);
    }
}

@keyframes pulsar {
    0%, 100% {
        transform: translate(-50%, -50%) scale(.90);
        opacity: .75;
    }

    50% {
        transform: translate(-50%, -50%) scale(1.15);
        opacity: 1;
    }
}

/* CHAT */

[data-testid="stChatMessage"] {
    background:
        linear-gradient(
            90deg,
            rgba(0, 80, 120, .12),
            rgba(0, 15, 25, .72)
        );

    border: 1px solid rgba(0, 190, 255, .20);
    border-left: 2px solid #00a9df;

    border-radius: 3px;

    backdrop-filter: blur(8px);

    box-shadow:
        0 0 15px rgba(0, 190, 255, .04);
}

/* INPUT */

[data-testid="stChatInput"] {
    background: rgba(0, 10, 18, .96);

    border: 1px solid rgba(0, 190, 255, .50);

    border-radius: 3px;

    box-shadow:
        0 0 18px rgba(0, 190, 255, .12);
}

/* MOBILE */

@media (max-width: 700px) {

    .hud {
        height: 310px;
    }

    .hud-circle-1 {
        width: 210px;
        height: 210px;
    }

    .hud-circle-2 {
        width: 160px;
        height: 160px;
    }

    .hud-circle-3 {
        width: 110px;
        height: 110px;
    }

    .hud-circle-4 {
        width: 70px;
        height: 70px;
    }

    .left-panel,
    .right-panel,
    .hud-label-left,
    .hud-label-right {
        display: none;
    }

    .valtair-title {
        font-size: 24px;
        letter-spacing: 8px;
    }
}

</style>
""", unsafe_allow_html=True)


    # =====================================================
    # HTML DO HUD
    # IMPORTANTE: SEM ESPAÇOS NO COMEÇO DAS LINHAS
    # =====================================================

    html_hud = """
<div class="valtair-title">VALTAIR</div>
<div class="valtair-subtitle">VIRTUAL ARTIFICIAL INTELLIGENCE SYSTEM</div>
<div class="hud">
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
<div class="hud-label-left">SYS.01 // NEURAL INTERFACE</div>
<div class="hud-label-right">VOICE LINK // CONNECTED</div>
<div class="hud-circle-1"></div>
<div class="hud-circle-2"></div>
<div class="hud-circle-3"></div>
<div class="hud-circle-4"></div>
<div class="hud-core"></div>
<div class="core-status">● VALTAIR ONLINE</div>
</div>
"""

    st.markdown(
        html_hud,
        unsafe_allow_html=True
    )

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
