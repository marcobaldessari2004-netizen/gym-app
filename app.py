import streamlit as st
import google.generativeai as genai

st.title("La mia AI Personale 🤖")

# Configurazione semplice
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("AI Connessa!")
    else:
        st.error("Chiave API mancante nei Secrets.")
except Exception as e:
    st.error(f"Errore configurazione: {e}")

# Inizializzazione messaggi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input utente
if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Risposta AI (solo se il modello è attivo)
    if "model" in locals():
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.write(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Errore risposta: {e}")
