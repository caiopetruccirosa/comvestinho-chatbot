# =========
#  Imports
# =========

# Fix Chroma and SQLite3 issue with StreamLit
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import dotenv

from comvestinhochatbot import ComvestinhoChatBot

# =========
#  ChatBot
# =========

@st.cache_resource
def load_comvestinho_chatbot():
    return ComvestinhoChatBot()

# Load OPENAI_API_KEY environment variable in .env file
dotenv.load_dotenv()

# Init and run conversational bot
comvestinho_chatbot = load_comvestinho_chatbot()

# Add application title
st.title("Bem vindo ao ComvestinhoChatBot!")

# Initialize chat history if its a new session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Faça uma pergunta sobre o Vestibular da Unicamp 2024!"):
    # Display user message in chat message container
    # and add user message to chat history
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Ask ComvestinhoChatBot passing the users input
    response = comvestinho_chatbot.ask(prompt, st.session_state.chat_history)

    # Display assistant response in chat message container
    # and add assistant response to chat history
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})