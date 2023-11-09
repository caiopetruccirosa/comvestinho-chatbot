# Fix Chroma and SQLite3 issue with StreamLit
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -------------------------------------------

import streamlit as st
import dotenv

from comvestinhochatbot import ComvestinhoChatBot

# Load OPENAI_API_KEY environment variable in .env file
dotenv.load_dotenv()

# Initialize chat history
chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
role_map = { "user": "Usuário", "assistant": "Sistema"}
for message in st.session_state.messages:
    chat_history.append(f"{role_map[message['role']]}: {message['content']}")
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Init and run conversational bot
comvestinho = ComvestinhoChatBot(chat_history)

# Init components
st.title("Bem vindo ao ComvestinhoChatBot!")

# React to user input
if prompt := st.chat_input("Faça uma pergunta sobre o Vestibular da Unicamp 2024!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ask ComvestinhoChatBot passing the users input
    response = comvestinho.ask(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})