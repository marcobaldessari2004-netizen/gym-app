import streamlit as st
import google.generativeai as genai
import os

# Titolo della tua App
st.title("La mia AI Personale 🤖")

# Configurazione della chiave API dai Secrets di Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Scelta il modello Gemini 1.5 Flash
model = genai.GenerativeModel('gemini-1.5-flash')

# Inizializza la chat se non esiste nella sessione
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti della conversazione
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Casella di input per l'utente
if prompt := st.chat_input("Scrivi qui..."):
    # Aggiunge il messaggio dell'utente alla storia
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Genera la risposta dell'AI
    with st.chat_message("assistant"):
        try:
            # Prepara la storia della chat per il modello
            chat_history = [
                {"role": m["role"], "parts": [m["content"]]}
                for m in st.session_state.messages
            ]
            
            response = model.generate_content(chat_history)
            st.write(response.text)
            
            # Salva la risposta dell'AI nella storia
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"Errore: {e}")
