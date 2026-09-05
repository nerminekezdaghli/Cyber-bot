import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

st.set_page_config(page_title="Cyber-Bot", page_icon="🤖")
st.title("Cyber-Bot 🤖")
st.caption("Votre assistant intelligent pour la technologie et la vie quotidienne")


def get_api_key() -> str:
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
        raise RuntimeError("GEMINI_API_KEY is not configured")


@st.cache_resource
def get_client() -> genai.Client:
    return genai.Client(api_key=get_api_key())


system_prompt = """You are Cyber-Bot, a friendly and intelligent public AI assistant.
Help with everyday life, technology, programming, AI, electronics, science,
education, entertainment, gaming, productivity, and general knowledge.
Answer clearly, respectfully, and in the same language as the user.
Support English, French, Arabic, and Tunisian Arabic."""


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Écrivez votre message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = get_client().models.generate_content(
            model="gemini-3.6-flash",
            contents=f"{system_prompt}\n\nUser message:\n{prompt}",
        )
        answer = (response.text or "").strip()
        if not answer:
            raise RuntimeError("Gemini returned an empty response")
    except Exception as error:
        answer = "Désolé 😕 Une erreur s'est produite. Vérifiez la configuration de Gemini."
        st.error(str(error))

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
